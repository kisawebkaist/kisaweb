from django.urls import path

#from .views import post_view, category_view, blog_view, delete_post, PostCreate, PostUpdate, PostCategoryCreate
from .views import post_view, blog_view

urlpatterns = [
    path('view/<slug:post_slug>/', post_view, name='post'),
    path('view/', blog_view, name='blog'),
    #path('view/<slug:category_slug>/', category_view, name='category'),
    #path('modify/<slug:category_slug>/<slug:post_slug>/', PostUpdate.as_view(), name='modify'),
    #path('delete/<slug:category_slug>/<slug:post_slug>/', delete_post, name='delete'),
    #path('create/post/', PostCreate.as_view(), name='create_post'),
    #path('create/category/', PostCategoryCreate.as_view(), name='create_category'),
]
