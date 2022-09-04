from django.urls import path
from .views import URLShortenerView

urlpatterns = [
    path('<str:name>', view = URLShortenerView.as_view(), name = 'url-shortener')
]
