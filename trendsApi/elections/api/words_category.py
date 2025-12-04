from ..models import Category, Word
from rest_framework import viewsets, serializers
from rest_framework.permissions import AllowAny
import django_filters.rest_framework


class WordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Word
        fields = '__all__'


class WordCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = WordSerializer
    model = Word
    http_method_names = ['get', 'head']
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('period',)

    def get_queryset(self):
        period = self.request.query_params.get('period', None)
        queryset = Word.objects.none()

        if not period:
            period = 'today 1-m'
        second_round = self.request.query_params.get('round', None)
        for category in Category.objects.all():
            query = Word.objects.filter(category=category, period=period).distinct('text').order_by(
                'text')
            if second_round:
                query = query.filter(candidate__second_round=True)
            queryset = queryset.union(query[:30])
        return queryset
