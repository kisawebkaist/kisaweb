from django.urls import path

from . import views

urlpatterns = [
    path('state', views.get_state_view, name='state'),
    path('misc/<slug:slug>', views.get_misc_view, name='misc')
]
