from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone, dateformat

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
    viewed_candidate = Candidate.objects.get(name=name.replace('-', ' '))
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

KISA_MEMBERS = []

@login_required
@require_http_methods(['POST'])
def vote(request, name):
    def format(val):
        return int(dateformat.format(val, 'YmdHis'))

    voted_candidate = Candidate.objects.get(name=name.replace('-', ' '))
    user = request.user
    if not hasattr(user, 'voter'):
        if len(Candidate.objects.all()) > 1:
            latest_election = Election.objects.latest('start_datetime')
            if user.is_staff:
                voter = Voter.objects.create(user=user, voted_candidate=voted_candidate)
                voter.save()
                voted_candidate.vote()
                messages.success(request, f'Successfully voted for {str(voted_candidate)}!', extra_tags='success')
            elif format(timezone.now()) < format(latest_election.start_datetime) or format(timezone.now()) > format(latest_election.end_datetime):
                messages.error(request, f'Voting is not open. Please check the election timeline.', extra_tags='danger')
            else:
                if user.email in KISA_MEMBERS:
                    voter = Voter.objects.create(user=user, voted_candidate=voted_candidate, is_kisa=True)
                else:
                    voter = Voter.objects.create(user=user, voted_candidate=voted_candidate)
                voter.save()
                voted_candidate.vote()
                messages.success(request, f'Successfully voted for {str(voted_candidate)}!', extra_tags='success')
        else:
            latest_election = Election.objects.latest('start_datetime')
            if format(timezone.now()) < format(latest_election.start_datetime) or format(timezone.now()) > format(latest_election.end_datetime):
                return HttpResponse('novote')
            vote_type = request.POST.get('type')
            voter = Voter.objects.create(user=user, voted_candidate=voted_candidate, vote_type=vote_type)
            voter.save()
            if vote_type == 'yes':
                voted_candidate.vote_yes()
            elif vote_type == 'no':
                voted_candidate.vote_no()
            else:
                return redirect(reverse('election'))
            return HttpResponse('Success')
    return redirect(reverse('election'))


@login_required
@require_http_methods(['POST'])
def change_embed_ratio(request, pk=None):
    if pk:
        model = Candidate.objects.get(pk=pk)
    else:
        print('DEBUG: This should\'nt happen!!!!')
    return redirect(reverse('election', kwargs={'semyear': semyear}))
