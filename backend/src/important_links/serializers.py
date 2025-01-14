import rest_framework.serializers as serializer
from .models import LinkCategory, Link

class LinkCategorySerializer(serializer.ModelSerializer):
    class Meta:
        model = LinkCategory
        fields = [ 'title_category', 'id' ]

class LinkSerializer(serializer.ModelSerializer):
    class Meta:
        model = Link
        fields = [
            'title',
            'url',
            'description',
            'category',
            'is_english',
            'requires_sso',
            'external_access'
        ]
