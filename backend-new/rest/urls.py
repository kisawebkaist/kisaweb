from django.urls import re_path
from rest_framework.routers import DefaultRouter
from rest import views

urlpatterns = [
    re_path(r'misc/*', views.MiscAPIView.as_view())
]