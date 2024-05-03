import rest_framework.serializers as serializer
from .models import FAQ, Category

class FaqSerializer(serializer.ModelSerializer):
    class Meta:
        model = FAQ
        fields = [
            'question', 'timestamp', 'answer', 'category', 'id'
        ]

class FaqCategorySerializer(serializer.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'title_category', 'id'
        ]
