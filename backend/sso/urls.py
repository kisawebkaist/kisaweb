from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_view, name='klogin'),
    path('login-response/', views.login_response_view, name='klogin-response'),
    path('logout/', views.logout_view, name='klogout'),
]
