from django.shortcuts import render, HttpResponse, redirect

from .models import Text, Title

def aboutus(request):
    title = Title
    context = {'Title: ': title}
    return render(request, 'aboutus/aboutus.html', context)