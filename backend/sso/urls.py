from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('login-response/', views.login_response_view, name='login-response'),
    path('login-error/', views.login_error_view, name='login-error'),
    path('logout/', views.logout_view, name='logout'),
]
