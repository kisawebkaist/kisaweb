from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest import views

router = DefaultRouter()
router.register(r'navbar', views.NavBarViewSet, basename="navbar")
router.register(r'footer', views.FooterViewSet, basename="footer")

urlpatterns = [
    path('misc/', include(router.urls))
]