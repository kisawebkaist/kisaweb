from django.urls import path

from . import views
from rest_framework.routers import DefaultRouter

# API
router = DefaultRouter()
router.register(
    'content', views.PostViewSet, basename = 'blog-post'
)
router.register(
    'tags', views.PostTagViewSet, basename = 'blog-post-tags'
)
urlpatterns = router.urls
