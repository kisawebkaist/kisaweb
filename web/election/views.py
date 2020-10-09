from django.shortcuts import render, HttpResponse

from .models import Election

# Create your views here.

def election(request, semyear):
    latest_election = Election.objects.latest('start_datetime')

    context = {
        'election': latest_election,
    }
    return render(request, 'election/election.html', context)

def candidate(request, name):
    latest_election = Election.objects.latest('start_datetime')

    context = {
        'election': latest_election,
    }
    return render(request, 'election/candidate.html', context)
