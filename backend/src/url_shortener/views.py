from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpRequest
from .models import UrlShortener

def get_ip_address(request : HttpRequest) -> str:
    try:
        return request.META['HTTP_X_FORWARDED_FOR'].split(',')[0]
    except KeyError:
        return request.META['REMOTE_ADDR']

class URLShortenerView(APIView):
    def get(self, request : HttpRequest, name : str):
        url         = UrlShortener.objects.filter(name = name)
        url         = get_object_or_404(url)
        ip_address  = get_ip_address(request)
        url.visit(ip_address)
        return Response(
            status = status.HTTP_200_OK,
            data = url.target
        )
