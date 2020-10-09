from django.shortcuts import HttpResponse
from django.utils import timezone

from election.models import Election

# def navbar_election_link_visible(request):
#     latest_election = Election.objects.latest('start_datetime')
#     semyear = str(latest_election).replace(' ', '-')
#     now = timezone.now()
#     # visible = now >= latest_election.start_datetime and now <= latest_election.end_datetime
#     visible = True
#     return {
#         'election_link_visible': visible,
#         'election_semyear': semyear,
#     }
#     return True
