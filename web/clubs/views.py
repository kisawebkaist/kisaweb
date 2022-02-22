from multiprocessing import context
from django.shortcuts import render, HttpResponse
from .models import Club

# Create your views here.
def clubs(request, cat=None):
    return render(request, "clubs/homepage.html")

def showcat(request, cat):
    query = Club.objects.filter(catagory=cat)
    if query == None:
        return HttpResponse("Page not found", status=404)

    names = []
    emails = []
    catagory = []
    slogans = []
    images = []
    informations = []

    for i in query:
        names.append(i.name)
        emails.append(i.email)
        catagory.append(i.catagory)
        slogans.append(i.slogan)
        images.append(i.image.url)
        informations.append(i.information)
    
    queries = zip(names, emails, catagory, slogans, images, informations)

    context = {
        'queries': queries,
        'catagory': cat
        } 
    print(context)
    return render(request, "clubs/base2.html", context)
    
    