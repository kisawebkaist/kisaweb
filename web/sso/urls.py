from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.sso_login_redirect, name='login'),
    path('logout/', views.sso_logout_redirect, name='logout'),
    path('login-response/', views.sso_login_response, name='sso_login_response'),
    path('logout-response/', views.sso_logout_response, name='sso_logout_response')
]
