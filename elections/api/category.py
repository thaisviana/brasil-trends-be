from ..models import Category, Word
from .candidate_words import WordSerializer
from rest_framework import viewsets, serializers
from rest_framework.permissions import AllowAny


class CategorySerializer(serializers.ModelSerializer):
    category_words = WordSerializer(Word.objects.filter(status=True)[:16], many=True, read_only=True,)

    class Meta:
        model = Category
        fields = '__all__'


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer
    model = Category
    http_method_names = ['get', 'head']

    def get_queryset(self):
        return Category.objects.all()
