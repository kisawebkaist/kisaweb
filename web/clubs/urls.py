from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.clubs),
    path('<str:cat>', views.showcat, name='club_page'),
    path('faicon/', include('faicon.urls')),
]
