from ..models import Candidate
from rest_framework import viewsets, serializers
from rest_framework.permissions import AllowAny

import django_filters.rest_framework


class CandidateLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        exclude = ('top', 'left')


class CandidateLightViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = CandidateLightSerializer
    model = Candidate
    http_method_names = ['get', 'head']
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('words__period', 'slug',)

    def get_queryset(self):
        queryset = Candidate.objects.filter(active=True).order_by('-size')
        second_round = self.request.query_params.get('round', None)
        election_year = self.request.query_params.get('election_year', None)

        if second_round:
            queryset = queryset.filter(second_round=True)
        
        if election_year:
            queryset = queryset.filter(election_year=election_year)

        return queryset
