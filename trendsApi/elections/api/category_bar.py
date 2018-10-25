from elections.models import Word, Candidate, Category
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.cache import cache
import trendsApi.settings as settings


def get_bar_chart_yearly():
    return get_bar_chart('today 1-y')

def get_bar_chart_monthly():
    return get_bar_chart('today 1-m')

def get_bar_chart_weekly():
    return get_bar_chart('now 7-d')


def get_bar_chart(period, second_round=False):
    result = []
    values = []
    for c in Category.objects.all():
        category = {'name': c.text, 'id': c.id}
        total = sum(Word.objects.filter(period=period, category=c).values_list('size', flat=True))
        candidates = Candidate.objects.filter(active=True)
        if second_round:
            candidates = candidates.filter(second_round=True)
        for candidate in candidates:
            c_amount = sum(Word.objects.filter(period=period, category=c, candidate=candidate).values_list('size', flat=True))
            category.setdefault('values', []).append(
                {'id': str(candidate.id),
                 'title': candidate.name,
                 'slug': candidate.slug,
                 'color': candidate.color,
                 'value': round(c_amount/total, 2) * 100}
            )
            values.append(round(c_amount/total, 2) * 100)
            category['max_value'] = max(values)
        result.append(category)
    return result


@api_view(['GET'])
@permission_classes((AllowAny, ))
def bar_view(request):
    period = request.query_params.get('period', None)
    if not period:
        period = 'today 1-m'
    if period == 'today 1-y':
        cache_key = 'yearly_bar'
        function = get_bar_chart_yearly()
    if period == 'today 1-m':
        cache_key = 'monthly_bar'
        function = get_bar_chart_monthly()
    if period == 'now 7-d':
        cache_key = 'weekly_bar'
        function = get_bar_chart_weekly()
    result = cache.get(cache_key)
    if result is None:
        result = function
        cache.set(cache_key, result, settings.CACHE_TIME)
        print("new result")
    return Response(result)

@api_view(['GET'])
@permission_classes((AllowAny, ))
def bar_r2_view(request):
    period = request.query_params.get('period', None)
    if not period:
        period = 'today 1-m'
    result = get_bar_chart(period, True)
    return Response(result)


