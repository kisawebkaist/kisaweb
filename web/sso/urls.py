from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.SSOLoginRedirect.as_view(), name='login'),
    path('logout/', views.sso_logout_redirect, name='logout'),
    path('logout-response/', views.sso_logout_response, name='sso_logout_response')
]
