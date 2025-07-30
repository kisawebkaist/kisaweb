from django.urls import path
from .views import alumni_api_view

urlpatterns = [
    path('', alumni_api_view, name='alumni')
]
