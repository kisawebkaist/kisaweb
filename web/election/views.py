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
    the system, to vote for the candidates.
    According to the status of the user,
    this method either creates a "Voter" 
    object and associate it with the user; or 
    alert the user.
'''

@login_required
@require_http_methods(['POST'])
def vote(request, name):
    latest_election = Election.objects.latest('start_datetime')
    semyear = str(latest_election).split()[1]
    voted_candidate = Candidate.objects.get(name=name) 
    user = request.user
    if not Voter.objects.filter(user=user).exists():
        Voter.objects.create(user=user, voted_candidate=voted_candidate)
        user.voter.save()
        messages.success(request, 'Successfully voted for ' + str(voted_candidate) + '!', extra_tags='success')
    else:
        messages.error(request, 'You have already voted for ' + str(user.voter.voted_candidate) + '!', extra_tags='danger')
    return redirect(reverse('election', kwargs={'semyear': semyear})) 