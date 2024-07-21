from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Multimedia
from .serializers import MutlimediaSerializer
class MultimediaViewSet(ReadOnlyModelViewSet):
    serializer_class = MutlimediaSerializer
    queryset = Multimedia.objects.all()
    lookup_field = 'slug'