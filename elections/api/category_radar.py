from elections.models import Word, Candidate, Category
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.cache import cache
import trendsApi.settings as settings


def get_candidate_categories_percents_monthly():
    return get_candidate_categories_percents('today 1-m')


def get_candidate_categories_percents_weekly():
    return get_candidate_categories_percents('now 7-d')


def get_candidate_categories_percents_yearly():
    return get_candidate_categories_percents('today 1-y')


def get_candidate_categories_percents(period, second_round=False):
    result = []
    candidates = Candidate.objects.filter(active=True)
    if second_round:
        candidates = candidates.filter(second_round=True)
    for candidate in candidates:
        candidate_words = {'id': candidate.id, 'name': candidate.name, 'color': candidate.color}
        categories = []
        ws = Word.objects.filter(candidate_id=candidate.id, period=period)
        total = sum(ws.values_list('size', flat=True))
        for category in Category.objects.all():
            wpc = ws.filter(category=category)
            wpc = sum(wpc.values_list('size', flat=True))
            if total == 0:
                percent = 1
            else:
                percent = round((wpc / total) * 100, 2)
                percent = percent if percent != 0 else 1
            categories.append({'name': category.text,
                               'id': category.id,
                               'percent': percent
                               })
        candidate_words['categories'] = categories
        result.append(candidate_words)
    return result


@api_view(['GET'])
@permission_classes((AllowAny, ))
def radar_view(request):
    period = request.query_params.get('period', None)
    if not period:
        period = 'today 1-m'
    if period == 'today 1-y':
        cache_key = 'yearly_radar'
        function = get_candidate_categories_percents_yearly()
    if period == 'today 1-m':
        cache_key = 'monthly_radar'
        function = get_candidate_categories_percents_monthly()
    if period == 'now 7-d':
        cache_key = 'weekly_radar'
        function = get_candidate_categories_percents_weekly()
    result = cache.get(cache_key)
    if result is None:
        result = function
        cache.set(cache_key, result, settings.CACHE_TIME)
    return Response(result)



@api_view(['GET'])
@permission_classes((AllowAny, ))
def radar_r2_view(request):
    period = request.query_params.get('period', None)
    if not period:
        period = 'today 1-m'
    result = get_candidate_categories_percents(period, True)
    return Response(result)
