from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('login-response/', views.login_response_view, name='login-response'),
    path('login-handler/', views.login_handler_view, name='login-handler'),
    path('login-error/', views.login_error_view, name='login-error'),
    path('logout/', views.logout_view, name='logout'),
    path('logout-response/', views.logout_response_view, name='logout-response'),
]
