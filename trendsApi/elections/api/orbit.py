from elections.models import Word, Candidate
from elections.service import ElectionService
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


def remove_duplicates(words):
    without_duplicates = []
    for w in words:
        if w[0] not in [word['text'] for word in without_duplicates]:
            c = ElectionService.get_candidate_by_name(w[0])
            size = 100 - w[1]
            without_duplicates.append({
                'text': w[0],
                'size': size if size == 0 else 1,
                'is_candidate': c.id if c else None})
    return without_duplicates[:9]


@api_view(['GET'])
@permission_classes((AllowAny, ))
def orbit_view(request):
    result = []
    candidate_id = request.query_params.get('candidate', None)
    period = request.query_params.get('period', None)
    if not period:
        period = 'today 1-m'
    if candidate_id:
        candidates = Candidate.objects.filter(id=int(candidate_id))
    else:
        candidates = Candidate.objects.filter(active=True)
    second_round = request.query_params.get('round', None)
    if second_round:
        candidates = candidates.filter(second_round=True)
    for c in candidates:
        orbit = {'id': c.id,
                 'name': c.name,
                 'color': c.color,
                 'people': remove_duplicates(Word.objects.filter(category_id__in=[6, 3],
                                                                 period=period,
                                                                 candidate_id=c.id)
                                             .order_by('-size').values_list('text', 'size',  flat=False))
                 }
        result.append(orbit)
    return Response(result)


