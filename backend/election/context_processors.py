from django.shortcuts import HttpResponse
from django.utils import timezone

from election.models import Election

def navbar_election_link_visible(request):
    if Election.objects.all().exists():
        latest_election = Election.objects.latest('start_datetime')
        visible = latest_election.is_open_public
        if request.user.is_authenticated and request.user.has_perm('election.preview_election'):
            visible = True
    else:
        visible = False
    return {
        'election_link_visible': visible,
    }
