from ..models import ImportantDates
from rest_framework import viewsets, serializers
from rest_framework.permissions import AllowAny
import django_filters.rest_framework
from django.db.models.functions import TruncDate


class ImportantDatesSerializer(serializers.ModelSerializer):
    day = serializers.SerializerMethodField()

    def get_day(self, obj):
        return obj.day

    class Meta:
        model = ImportantDates
        fields = '__all__'


class ImportantDatesViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = ImportantDatesSerializer
    model = ImportantDates
    http_method_names = ['get', 'head']
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)

    def get_queryset(self):
        return ImportantDates.objects.filter(confirmed=True).annotate(day=TruncDate('date'))