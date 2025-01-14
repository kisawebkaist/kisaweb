from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework import filters
from .serializers import  PostTagSerializer, PostAllSerializer, PostSerializer
from .models import Post, PostTag

class PostViewSet(ModelViewSet):
    serializer_class = PostAllSerializer
    queryset = Post.objects.all().order_by('-created')
    filter_backends = [ filters.SearchFilter ]
    lookup_field = 'slug'
    search_fields = [ 'title', 'tags__tag_name' ]

    def get_serializer_class(self):
        if self.action == 'list':
            return PostAllSerializer
        else:
            return PostSerializer

class PostTagViewSet(ReadOnlyModelViewSet):
    serializer_class = PostTagSerializer
    queryset = PostTag.objects.all()
    filter_backends = [ filters.SearchFilter ]
    search_fields = [ 'tag_name' ]
