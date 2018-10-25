from functools import reduce
from django.db.models import Q
from elections.models import Word, Candidate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


def remove_duplicates(words):
    without_duplicates = []
    for w in words:
        if w[0] not in [word['text'] for word in without_duplicates]:
            without_duplicates.append({'text': w[0], 'size': w[1]})
    return without_duplicates


@api_view(['GET'])
@permission_classes((AllowAny, ))
def list_relationship_view(request):
    c1 = request.query_params.get('c1', None)
    c2 = request.query_params.get('c2', None)
    result = {}

    words_c1 = Word.objects.filter(candidate_id=c1).order_by('-size')
    c1 = Candidate.objects.get(id=c1)

    if c2 is None:
        result['candidato_1'] = {'words':  remove_duplicates(words_c1.values_list('text', 'size',  flat=False))[:11],
                                 'color': c1.color,
                                 'name': c1.name}
        return Response(result)

    words_c2 = Word.objects.filter(candidate_id=c2).order_by('-size')

    c2 = Candidate.objects.get(id=c2)
    text_c1 = words_c1.values_list('text', flat=True)
    text_c2 = words_c2.values_list('text', flat=True)
    input_list = [text_c1, text_c2]
    intersection = reduce(set.intersection, map(set, input_list))

    words_c1 = words_c1.filter(~Q(text__in=intersection)).values_list('text', 'size',  flat=False)
    words_c2 = words_c2.filter(~Q(text__in=intersection)).values_list('text', 'size',  flat=False)

    result['candidato_1'] = {'words': remove_duplicates(words_c1)[:11], 'color': c1.color, 'name': c1.name}
    result['candidato_2'] = {'words': remove_duplicates(words_c2)[:11], 'color': c2.color, 'name': c2.name}
    result['intersection'] = list(intersection)[:11]
    return Response(result)


