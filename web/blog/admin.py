from django.contrib import admin
from .models import Post, PostTag

'''
  This file contains which fields of a model to be
  shown on the admin panel to be edited/value assigned.
'''

# Register your models here.

class PostAdmin(admin.ModelAdmin):
  list_display = ['title', 'slug', 'get_tags']
  
  def get_tags(self, obj):
    return ['#' + p.tag_name for p in obj.tags.all()]

class PostTagAdmin(admin.ModelAdmin):
  list_display = ['tag_name']

admin.site.register(Post, PostAdmin)
admin.site.register(PostTag, PostTagAdmin)