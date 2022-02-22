from django.urls import path
from . import views

urlpatterns = [
    path('', views.clubs),
    path('<str:cat>', views.showcat, name='club_page')
]
