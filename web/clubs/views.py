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

    # queries = zip(names, emails, catagory, slogans, images, informations)

    context = {
        'queries': query,
        'catagory': cat
        } 
    print(context)
    return render(request, "clubs/clublist.html", context)
    
    