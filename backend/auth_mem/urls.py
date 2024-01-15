from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('check-username', views.check_username_view, name='check-username'),
    path('signup', views.signup_view, name='signup'),
    path('register-mail', views.register_mail_view, name='register-mail'),
    path('attempt-mail-reg', views.attempt_mail_reg_view, name='attempt-mail-reg'),
    path('change-pw', views.change_pw_view, name='change-pw'),
    path('attempt-pw-change', views.attempt_pw_change_view, name='attempt-pw-change')
]