from .models import Post, PostTag
import rest_framework.serializers as serializer

class PostTagSerializer(serializer.ModelSerializer):
    class Meta:
        model = PostTag
        fields = ['tag_name', ]

class PostAllSerializer(serializer.Serializer):
    tags = PostTagSerializer(many = True)
    class Meta:
        model = Post
        fields = [
            'title', 'description', 'created', 'modified', 'slug', 'tags'
        ]

class PostSerializer(serializer.Serializer):
    tags = PostTagSerializer(many = True, required = False)
    class Meta:
        model = Post
        fields = [
            'title',
            'description',
            'content',
            'new_content',
            'created',
            'modified',
            'slug',
            'tags'
        ]
        extra_kwargs = {
            'title' : {'required' : False},
            'description' : {'required' : False},
            'created' : {'required' : False},
            'modified' : {'required' : False},
            'slug' : {'required' : False},
            'content' : {'required' : False}
        }
