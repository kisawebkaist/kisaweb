from django.urls import path
from .views import alumni_view

urlpatterns = [
    path('', alumni_view, name='alumni')
]
