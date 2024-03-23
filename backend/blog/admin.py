from django.contrib import admin
from .models import Post, PostTag
from django import forms
from django_draftjs import EditorWidget

'''
    This file contains which fields of a model to be
    shown on the admin panel to be edited/value assigned.
'''

# Register your models here.
class PostForm(forms.ModelForm):
    new_content = forms.JSONField(widget = EditorWidget())
    class Meta:
        model = Post
        fields = [
            'title',
            'description',
            'tags',
            'image',
            'new_content',
        ]
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'get_tags']
    readonly_fields = ['created', 'modified', 'slug']
    form = PostForm
    def get_tags(self, obj):
        return ['#' + p.tag_name for p in obj.tags.all()]

@admin.register(PostTag)
class PostTagAdmin(admin.ModelAdmin):
    list_display = ['tag_name']
