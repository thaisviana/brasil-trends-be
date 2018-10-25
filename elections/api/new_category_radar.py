from elections.models import Word, Candidate, Category
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.cache import cache
import trendsApi.settings as settings


def get_new_candidate_categories_percents_monthly():
    return get_new_candidate_categories_percents('today 1-m')


def get_new_candidate_categories_percents_weekly():
    return get_new_candidate_categories_percents('now 7-d')


def get_new_candidate_categories_percents_yearly():
    return get_new_candidate_categories_percents('today 1-y')


def get_new_candidate_categories_percents(period):
    result = []
    for candidate in Candidate.objects.filter(active=True):
        candidate_words = {'id': candidate.id,
                           'name': candidate.name,
                           'color': candidate.color,
                           'active': candidate.active}
        categories = []
        ws = Word.objects.filter(candidate_id=candidate.id,
                                 period=period,
                                 category_id__in=[1, 3, 4, 5, 6])
        total = sum(ws.values_list('size', flat=True))
        for category in Category.objects.filter(id__in=[1, 3, 4, 5, 6]):
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
def new_radar_view(request):
    period = request.query_params.get('period', None)
    if not period:
        period = 'today 1-m'
    if period == 'today 1-y':
        cache_key = 'yearly_radar'
        function = get_new_candidate_categories_percents_yearly()
    if period == 'today 1-m':
        cache_key = 'monthly_radar'
        function = get_new_candidate_categories_percents_monthly()
    if period == 'now 7-d':
        cache_key = 'weekly_radar'
        function = get_new_candidate_categories_percents_weekly()
    result = cache.get(cache_key)
    if result is None:
        result = function
        cache.set(cache_key, result, settings.CACHE_TIME)
    return Response(result)


