from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpRequest

from .models import UrlShortener

def get_ip_address(request : HttpRequest) -> str:
    try:
        return request.META['HTTP_X_FORWARDED_FOR'].split(',')[0]
    except KeyError:
        return request.META['REMOTE_ADDR']

class URLShortenerView(View):
    def get(self, request : HttpRequest, name : str):
        url         = UrlShortener.objects.filter(name = name)
        url         = get_object_or_404(url)
        ip_address  = get_ip_address(request)
        url.visit(ip_address)
        return redirect(to = url.target)
