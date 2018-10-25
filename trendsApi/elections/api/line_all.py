from elections.models import SizeHistory, Candidate, SizeHistorySecondRound
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from datetime import datetime, timedelta
from rest_framework.response import Response
from decimal import Decimal
from django.db.models import Max
from django.db.models.functions import TruncDate
from django.utils import timezone

map_period = {'today 1-y': 365,
              'today 1-m': 30,
              'now 7-d': 9,
              'now 1-d': 2,
              }

@api_view(['GET'])
@permission_classes((AllowAny, ))
def list_aggregated_lines_view(request):
    period = request.query_params.get('period', None)
    if not period:
        period = 'today 1-m'
    haddad = request.query_params.get('haddad', None)
    haddad = True if not haddad else False
    result = []

    range = datetime(2018, 10, 9) - timedelta(days=map_period[period])
    current_tz = timezone.get_current_timezone()
    range = current_tz.normalize(range.astimezone(current_tz))
    haddad_turn_day = datetime(2018, 8, 25)
    haddad_turn_day = current_tz.normalize(haddad_turn_day.astimezone(current_tz))

    second_round = request.query_params.get('round', None)
    candidates = Candidate.objects.filter(active=True)
    if second_round:
        candidates = candidates.filter(second_round=True)
        range = datetime.now() - timedelta(days=map_period[period])
    for c in candidates:
        candidate = {'name': c.name,
                     'id': c.id,
                     'color': c.color,
                     'period': period
                     }
        if not haddad:
            shs = SizeHistory.objects.filter(candidate=c, date__gte=range, weekly_size__isnull=False) \
                .annotate(day=TruncDate('date')).values('day') \
                .annotate(percent=Max('weekly_size')).values('day', 'percent').order_by('day')
        if haddad:
            shs = SizeHistory.objects.filter(candidate=c, date__gte=range,
                                             haddad_weekly_size__isnull=False)\
                .annotate(day=TruncDate('date')).values('day') \
                .annotate(percent=Max('haddad_weekly_size')).values('day', 'percent').order_by('day')
        if second_round:
            shs = SizeHistorySecondRound.objects.filter(candidate=c, date__gte=range,size__isnull=False)\
                .annotate(day=TruncDate('date')).values('day') \
                .annotate(percent=Max('size')).values('day', 'percent').order_by('day')
        aux_shs = []

        aux_shs.insert(0, {'percent': Decimal(0), 'day': range.date()})

        aux_shs.extend(list(shs))

        if second_round:
            aux_shs.append({'percent': Decimal(0), 'day': datetime.now().date()})
        else:
            aux_shs.append({'percent': Decimal(0), 'day': datetime(2018, 10, 9).date()})

        aux_shs.sort(key=lambda x: x['day'])
        candidate['lines'] = aux_shs
        result.append(candidate)
    return Response(result)
