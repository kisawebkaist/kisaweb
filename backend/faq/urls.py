from django.urls import path

from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(
    r'category', views.FaqCategoryViewset, basename = 'faq-category'
)
router.register('', views.FaqViewset, basename = 'faq')
urlpatterns = router.urls
