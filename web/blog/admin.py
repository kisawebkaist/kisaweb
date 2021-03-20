from django.contrib import admin
from .models import Post, PostCategory

'''
  This file contains which fields of a model to be
  shown on the admin panel to be edited/value assigned.
'''

# Register your models here.

class PostAdmin(admin.ModelAdmin):
  list_display = ['title', 'slug', 'author', 'category']

class PostCategoryAdmin(admin.ModelAdmin):
  list_display = ['name', 'slug', 'parent_category']

admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)