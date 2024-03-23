from django.urls import path
from . import views

# Set Up URLs:
# Configure the URL routing for your new app. You'll likely want to define a URL pattern that maps to a view responsible for handling image uploads. Add these URL configurations to image_uploader/urls.py.

urlpatterns = [
    path('', views.index, name='image_uploader'),
    path('upload/', views.upload, name='upload'),
    path('view_images/', views.view_images, name='view_images'),
]

