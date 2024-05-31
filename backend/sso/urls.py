from django.conf import settings
from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('login-response/', views.login_response_view, name='login-response'),
    path('logout/', views.logout_view, name='logout'),
    path('check-otp/', views.check_totp_view, name='check-otp'),
    path('change-otp-secret/', views.change_totp_secret, name='change-totp-secret'),
]

if hasattr(settings, "EMAIL_OTP_ENABLED") and settings.EMAIL_OTP_ENABLED:
    urlpatterns += [
        path('change-email/', views.change_email_view, name='change-email'),
        path('change-email-response/', views.change_email_response_view, name='change-email-response'),
        path('lost-totp-secret/', views.lost_totp_secret_view, name='lost-totp-secret'),
        path('lost-totp-secret-response/', views.lost_totp_secret_response_view, name='lost-totp-secret-response')
    ]