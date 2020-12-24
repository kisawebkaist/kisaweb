from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('validate/', views.validate_view, name='validate-sso'),
    path('agreement', views.agreement, name='sso-agreement'),
    path('error', views.login_error, name='login-error'),
]
