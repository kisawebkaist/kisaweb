from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone, dateformat

from .models import Election, Candidate, Voter

"""
Miko's formula
# of debate-attending kisa members = k
# of kisa members who dont attend debate + general votersv= g (treat those who dont attend debate as general voters) 

Formula = (#ofvoters from k/k + #of voters fromg/g )/2
"""

def get_weighted_result(candidate, election, **kwargs):
    
    all_voters = Voter.objects.filter(voted_election=election)

    general_vote_count_all = all_voters.filter(is_kisa=False, **kwargs).count()
    kisa_yes_debate_count_all = all_voters.filter(is_kisa=True, joined_debate=True, **kwargs).count()
    kisa_no_debate_count_all = all_voters.filter(is_kisa=True, joined_debate=False, **kwargs).count()

    general_vote_count = candidate.voters.filter(is_kisa=False, **kwargs).count()
    kisa_yes_debate_count = candidate.voters.filter(is_kisa=True, joined_debate=True, **kwargs).count()
    kisa_no_debate_count = candidate.voters.filter(is_kisa=True, joined_debate=False, **kwargs).count()

    general_vote_weight = election.general_vote_weight
    kisa_yes_debate_weight = election.kisa_yes_debate_weight
    kisa_no_debate_weight = election.kisa_no_debate_weight

    if not election.use_the_manual_weights: # Miko's formula
        try:
            general_vote_weight = 0.5 / (general_vote_count_all + kisa_no_debate_count_all)
        except:
            general_vote_weight = 0
        kisa_no_debate_weight = general_vote_weight
        try:
            kisa_yes_debate_weight = 0.5 / kisa_yes_debate_count_all
        except:
            kisa_yes_debate_weight = 0

    numerator = 0
    numerator += general_vote_count * general_vote_weight
    numerator += kisa_yes_debate_count * kisa_yes_debate_weight
    numerator += kisa_no_debate_count * kisa_no_debate_weight

    denominator = 0
    denominator += general_vote_count_all * general_vote_weight
    denominator += kisa_yes_debate_count_all * kisa_yes_debate_weight
    denominator += kisa_no_debate_count_all * kisa_no_debate_weight

    try:
        return float(numerator / denominator)
    except:
        return 0

# Create your views here.

def election(request):
    try:
        latest_election = Election.objects.latest('start_datetime')
    except Election.DoesNotExist:
        latest_election = None
    if request.user.is_authenticated and latest_election:
        has_voted = request.user.votes.filter(voted_election=latest_election).exists()
        is_open = request.user.has_perm('election.preview_election')
    else:
        has_voted = False
        is_open = False
    context = {
        'election': latest_election,
        'has_voted': has_voted
    }
    if latest_election is None:
        return render(request, 'election/election.html', context)
    
    is_open = is_open or latest_election.is_open_public

    context['is_open'] = is_open
    context['is_live'] = latest_election.start_datetime < timezone.now() < latest_election.end_datetime

    result_visible = latest_election.end_datetime < timezone.now()
    result_visible = result_visible and latest_election.results_out
    result_visible = result_visible or request.user.has_perm('election.see_election_results')
    
    context['result_visible'] = result_visible

    if latest_election.candidates.count() > 1: # Normal election
        candidate_list = latest_election.candidates.all()
        context['categories'] = [str(candidate) for candidate in candidate_list]
        context['filters'] = {
            'Weighted Votes': [get_weighted_result(candidate, latest_election) for candidate in candidate_list],
            'Non-KISA Votes': [candidate.voters.filter(is_kisa=False).count() for candidate in candidate_list],
            'KISA Votes': [candidate.voters.filter(is_kisa=True).count() for candidate in candidate_list],
        }
        if latest_election.show_debate_participation:
            context['filters']['KISA (in-debate) Votes'] = [candidate.voters.filter(is_kisa=True, joined_debate=True).count() for candidate in candidate_list]
    else: # Yes/No election TODO:
        candidate = latest_election.candidates.all()[0]
        context['categories'] = ["Yes", "No"]
        context['filters'] = {
            'Weighted Votes': [get_weighted_result(candidate, latest_election, vote_type=category) for category in ['yes', 'no']],
            'Non-KISA Votes': [candidate.voters.filter(vote_type=category, is_kisa=False).count() for category in ['yes', 'no']],
            'KISA Votes': [candidate.voters.filter(vote_type=category, is_kisa=True).count() for category in ['yes', 'no']],
        }
        if latest_election.show_debate_participation:
            context['filters']['KISA (in-debate) Votes'] = [candidate.voters.filter(vote_type=category, is_kisa=True, joined_debate=True).count() for category in ['yes', 'no']]
    
    context['explanations'] = {
        'Weighted Votes': latest_election.weighted_vote_explanation,
        'Non-KISA Votes': latest_election.non_kisa_vote_explanation,
        'KISA Votes': latest_election.kisa_vote_explanation
    }
    if latest_election.show_debate_participation:
        context['explanations']['KISA (in-debate) Votes'] = latest_election.kisa_in_debate_vote_explanation

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

@login_required
@require_http_methods(['POST'])
def vote(request, name):
    def format(val):
        return int(dateformat.format(val, 'YmdHis'))
    
    params = {
        'user': request.user,
        'voted_candidate': Candidate.objects.get(name=name.replace('-', ' ')),
        'voted_election': Election.objects.latest('start_datetime'),
    }

    if not params['user'].has_perm('election.voting_exception'):
        if params['user'].nationality == 'KOR':
            messages.error(request, 'Only international members of KAIST are eligible to vote.', extra_tags='danger')
            return redirect(reverse('election'))

        if not 'S' in params['user'].user_group: # Check whether an active student
            if not ('E' in params['user'].user_group and 'researcher' in params['user'].title_english.lower()): # Check whether the employee is a researcher
                messages.error(request, 'According to the rules, you are not eligible to vote. If you think this is a mistake, please contact the us at kisa@kaist.ac.kr.', extra_tags='danger')
                return redirect(reverse('election'))

    if params['user'].kaist_email is None:
        if not params['user'].is_staff: # If user is not staff, there is an error
            messages.error(request, 'There is a problem with your Kaist email provided through sso login. Please login again. If the problem persists, please contact the website administration.', extra_tags='danger')
            return redirect(reverse('election'))
        kaist_email = 'kisa@kaist.ac.kr'
    else:
        kaist_email = params['user'].kaist_email

    time_now = format(timezone.now())
    time_election_start = format(params['voted_election'].start_datetime)
    time_election_end = format(params['voted_election'].end_datetime)

    if not params['user'].votes.filter(voted_election=params['voted_election']).exists():
        if params['voted_election'].candidates.count() > 1:
            if time_now < time_election_start or time_now > time_election_end:
                messages.error(request, f'Voting is not open. Please check the election timeline.', extra_tags='danger')
            else:
                if params['voted_election'].kisa_member_email_list.find(kaist_email) != -1:
                    voter = Voter.objects.create(**params, is_kisa=True)
                else:
                    voter = Voter.objects.create(**params)
                voter.save()
                messages.success(request, f'Successfully voted for {str(params["voted_candidate"])}!', extra_tags='success')
        else:
            if time_now < time_election_start or time_now > time_election_end:
                messages.error(request, f'Voting is not open. Please check the election timeline.', extra_tags='danger')
                return HttpResponse('novote')
            vote_type = request.POST.get('type')
            if not (vote_type in ['yes', 'no']):
                messages.error(request, f'You cannot vote other than "Yes" or "No".', extra_tags='danger')
                return HttpResponse('novote')
            if params['voted_election'].kisa_member_email_list.find(kaist_email) != -1:
                voter = Voter.objects.create(**params, vote_type=vote_type, is_kisa=True)
            else:
                voter = Voter.objects.create(**params, vote_type=vote_type)
            voter.save()
            messages.success(request, f'Successfully voted "{vote_type.capitalize()}" for {str(params["voted_candidate"])}!', extra_tags='success')
            return HttpResponse('Success')
    else:
        messages.error(request, 'You have already voted.')
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
