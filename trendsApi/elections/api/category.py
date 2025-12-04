from ..models import Category, Word
from .candidate_words import WordSerializer
from rest_framework import viewsets, serializers
from rest_framework.permissions import AllowAny


class CategorySerializer(serializers.ModelSerializer):
    category_words = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'

    def get_category_words(self, obj):
        return WordSerializer(obj.words.all()[:16], many=True).data


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer
    model = Category
    http_method_names = ['get', 'head']

    def get_queryset(self):
        return Category.objects.all()
