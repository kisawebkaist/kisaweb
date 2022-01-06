from django.shortcuts import HttpResponse
from django.utils import timezone

from election.models import Election

def navbar_election_link_visible(request):
    if Election.objects.all().exists():
        latest_election = Election.objects.latest('start_datetime')
        # visible = now >= latest_election.start_datetime and now <= latest_election.end_datetime
        visible = latest_election.is_open
    else:
        visible = False
    return {
        'election_link_visible': visible,
    }
    # return True
