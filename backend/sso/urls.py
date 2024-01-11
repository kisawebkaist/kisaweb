from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_view, name='klogin'),
    path('login-response/', views.login_response_view, name='klogin-response'),
    path('login-error/', views.login_error_view, name='klogin-error'),
    path('logout/', views.logout_view, name='klogout'),
]
