from ..models import Candidate, Word
from rest_framework import viewsets, serializers
from rest_framework.permissions import AllowAny
import django_filters.rest_framework


class WordSerializer(serializers.ModelSerializer):
    color = serializers.SerializerMethodField()

    def get_color(self, obj):
        if obj.candidate:
            return obj.candidate.color
        return None

    class Meta:
        model = Word
        fields = '__all__'


class WordViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = WordSerializer
    model = Word
    http_method_names = ['get', 'head']
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('period', 'candidate',)

    def get_queryset(self):
        period = self.request.query_params.get('period', None)
        queryset = Word.objects.none()

        if not period:
            period = 'today 1-m'
        second_round = self.request.query_params.get('round', None)
        candidates = Candidate.objects.filter(active=True)
        if second_round:
            candidates = candidates.filter(second_round=True)
        for candidate in candidates:
            queryset = queryset.union(Word.objects.filter(candidate=candidate, period=period)[:16])
        return queryset


class CandidateSerializer(serializers.ModelSerializer):
    words = WordSerializer(Word.objects.all(), many=True, read_only=True,)

    class Meta:
        model = Candidate
        fields = '__all__'

    def get_words(self, obj):
        return WordSerializer(obj.words.all()[:16], many=True).data


class CandidateViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = CandidateSerializer
    model = Candidate
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('words__period', 'slug',)

    def get_queryset(self):
        second_round = self.request.query_params.get('round', None)
        candidates = Candidate.objects.filter(active=True)
        if second_round:
            candidates.filter(second_round=True)
        return candidates.order_by('-size')