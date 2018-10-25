from django.db.models import Max
from django.db.models.functions import TruncDate

from elections.models import SizeHistory, Candidate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework.response import Response
from decimal import Decimal


map_period = {'today 1-y': 365,
              'today 1-m': 32,
              'now 7-d': 9,
              'now 1-d': 1,
              }

@api_view(['GET'])
@permission_classes((AllowAny, ))
def list_individual_lines_view(request):
    candidate_id = request.query_params.get('candidate_id', None)
    period = request.query_params.get('period', None)
    if not period:
        period = 'today 1-m'
    result = {}
    if candidate_id:
        c = Candidate.objects.get(id=int(candidate_id))
        result = {'name': c.name,
                  'id': c.id,
                  'color': c.color,
                  'period': period}
        range = datetime.now() - timedelta(days=map_period[period])
        shs = SizeHistory.objects.filter(candidate=c, date__gte=range, weekly_size__isnull=False) \
            .annotate(day=TruncDate('date')).values('day')\
            .annotate(percent=Max('weekly_size')).values('day', 'percent').order_by('day')
        aux_shs = []

        current_tz = timezone.get_current_timezone()
        range = current_tz.normalize(range.astimezone(current_tz))

        first_node = list(filter(lambda x: x['day'] == range.date(), shs))

        if not first_node:
            aux_shs.insert(0, {'percent': Decimal(0), 'day': range.date()})

        aux_shs.extend(list(shs))

        last_node = list(filter(lambda x: x['day'] == range.date(), shs))

        if not last_node:
            aux_shs.append({'percent': Decimal(0), 'day': timezone.now().date()})

        aux_shs.sort(key=lambda x: x['day'])
        result['lines'] = shs
    return Response(result)


