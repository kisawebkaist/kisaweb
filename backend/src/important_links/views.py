from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Link, LinkCategory
from .serializers import LinkCategorySerializer, LinkSerializer

class LinkCategoryViewset(ReadOnlyModelViewSet):
    queryset = LinkCategory.objects.all()
    serializer_class = LinkCategorySerializer

class LinkViewset(ReadOnlyModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
