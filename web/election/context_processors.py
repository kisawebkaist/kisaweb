from django.shortcuts import HttpResponse
from django.utils import timezone

from election.models import Election

def navbar_election_link_visible(request):
    latest_election = Election.objects.latest('start_datetime')
    # visible = now >= latest_election.start_datetime and now <= latest_election.end_datetime
    visible = latest_election.is_open
    return {
        'election_link_visible': visible,
    }
    return True
