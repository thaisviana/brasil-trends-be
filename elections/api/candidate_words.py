from ..models import Candidate, Word
from rest_framework import viewsets, serializers
from rest_framework.permissions import AllowAny


class WordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Word
        fields = '__all__'


class WordViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = WordSerializer
    model = Word

    def get_queryset(self):
        return Word.objects.all()


class CandidateSerializer(serializers.ModelSerializer):
    words = WordSerializer(many=True, read_only=True)

    class Meta:
        model = Candidate
        fields = '__all__'


class CandidateViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = CandidateSerializer
    model = Candidate

    def get_queryset(self):
        return Candidate.objects.all()
