from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Election, Candidate, Voter

# Create your views here.

def election(request):
    try:
        latest_election = Election.objects.latest('start_datetime')
    except Election.DoesNotExist:
        latest_election = None
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
    voted_candidate = Candidate.objects.get(name=name)
    user = request.user
    if not hasattr(user, 'voter'):
        if len(Candidate.objects.all()) > 1:
            voter = Voter.objects.create(user=user, voted_candidate=voted_candidate)
            voter.save()
            voted_candidate.vote()
        else:
            vote_type = request.POST.get('type')
            voter = Voter.objects.create(user=user, voted_candidate=voted_candidate, vote_type=vote_type)
            voter.save()
            if vote_type == 'yes':
                voted_candidate.vote_yes()
            else:
                voted_candidate.vote_no()
            messages.success(request, f'Voted {vote_type} for {str(voted_candidate)}!', extra_tags='success')
            return redirect(reverse('election'))
        messages.success(request, f'Successfully voted for {str(voted_candidate)}!', extra_tags='success')
    return redirect(reverse('election'))


@login_required
@require_http_methods(['POST'])
def change_embed_ratio(request, pk=None):
    if pk:
        model = Candidate.objects.get(pk=pk)
    else:
        model = Election.objects.latest('start_datetime')
    response = model.change_embed_ratio(request.POST.get('ratio'))
    if not response: response = 'Success'
    return HttpResponse(response)
