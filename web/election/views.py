from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Election, Candidate, Voter

# Create your views here.

def election(request, semyear):
    latest_election = Election.objects.latest('start_datetime')
    context = {
        'election': latest_election,
        'has_voted': hasattr(request.user, 'voter'),
    }
    return render(request, 'election/election.html', context)

def candidate(request, name):
    viewed_candidate = Candidate.objects.get(name=name)
    latest_election = Election.objects.latest('start_datetime')
    context = {
        'election': latest_election,
        'candidate': viewed_candidate, 
    }
    return render(request, 'election/candidate.html', context)

'''
    "vote" method is designed for users logged in 
    the system and have never voted; to vote for the candidates.
    This method creates a "Voter" object and associate it with 
    the user.
'''

@login_required
@require_http_methods(['POST'])
def vote(request, name):
    latest_election = Election.objects.latest('start_datetime')
    semyear = str(latest_election).split()[1]
    voted_candidate = Candidate.objects.get(name=name) 
    user = request.user
    if not hasattr(user, 'voter'):
        Voter.objects.create(user=user, voted_candidate=voted_candidate)
        user.voter.save()
        messages.success(request, 'Successfully voted for ' + str(voted_candidate) + '!', extra_tags='success')
    else:
        print('DEBUG: This should\'nt happen!!!!')
    return redirect(reverse('election', kwargs={'semyear': semyear})) 