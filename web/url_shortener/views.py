from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpRequest

from .models import UrlShortener

class URLShortenerView(View):
    def get(self, request : HttpRequest, name : str):
        url     = UrlShortener.objects.filter(
            name = name
        )
        url     = get_object_or_404(url)
        return redirect(to = url.target)
