from django.urls import path

from .views import post_view, blog_view

urlpatterns = [
    path('view/<slug:post_slug>/', post_view, name='post_view'),
    path('view/', blog_view, name='blog'),
    #path('modify/<slug:category_slug>/<slug:post_slug>/', PostUpdate.as_view(), name='modify'),
    #path('delete/<slug:category_slug>/<slug:post_slug>/', delete_post, name='delete'),
    #path('create/post/', PostCreate.as_view(), name='create_post'),
    #path('create/category/', PostCategoryCreate.as_view(), name='create_category'),
]
