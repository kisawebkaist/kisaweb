from django.urls import path, include
# from django.contrib import admin
# from django.contrib.auth.views import LoginView

from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('course-resources/', views.course_resources, name='course_resources'),

    # path('events/', include('events.urls')),
    path('election/', include('election.urls')),
    path('docs/', include('docs.urls')),
    path('sso/', include('sso.urls')),
]
