from django.urls import path

from . import views

urlpatterns = [
    path('<str:semyear>/', views.election, name='election'),
    path('candidate/<str:name>', views.candidate, name='candidate'),
    path('candidate/<str:name>/vote', views.vote, name='vote'),
]
