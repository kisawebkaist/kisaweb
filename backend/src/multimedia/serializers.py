import rest_framework.serializers as serializer
from .models import *

class MultimediaImageSerializer(serializer.ModelSerializer):
    href = serializer.ImageField(source="file")
    class Meta:
        model = MultimediaImage
        fields = [
            "alt",
            "href",
            "date"
        ]

class MutlimediaSerializer(serializer.ModelSerializer):
    images = MultimediaImageSerializer(many = True)
    class Meta:
        model = Multimedia
        exclude = ["id"]
        