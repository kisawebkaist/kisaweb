from django.shortcuts import render, HttpResponse, redirect

from .models import Main, Members, Division

def aboutus(request):
    title = Main.title
    context = {'Title: ': title}
    return render(request, 'aboutus/aboutus.html', context)