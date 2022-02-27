from multiprocessing import context
from django.shortcuts import render, HttpResponse
from .models import Club, Catagory

# Create your views here.
def clubs(request, cat=None):
    query = Catagory.objects.all()
    if query == None:
        return HttpResponse("Page not found", status=404)
    context = {"catagories": query}

    return render(request, "clubs/homepage.html", context)

def showcat(request, cat):
    id = Catagory.objects.get(catagory_title=cat).id
    query = Club.objects.filter(catagory=id)
    if query == None:
        return HttpResponse("Page not found", status=404)

    context = {
        'queries': query,
        'catagory': cat,
        } 
    return render(request, "clubs/clublist.html", context)
    
    