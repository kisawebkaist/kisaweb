import datetime

from django.utils.translation import gettext as _

from rest_framework.decorators import authentication_classes, api_view
from rest_framework.exceptions import MethodNotAllowed, NotFound, PermissionDenied, ParseError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from core.utils import get_object_or_404
from sso.permissions import IsKAuthenticated
from sso.models import KAISTProfile

from .models import Election, Candidate, Vote, VotingExceptionToken
from .serializers import *

class ElectionInfoViewSet(ReadOnlyModelViewSet):
    serializer_class = ElectionInfoSerializer
    queryset = Election.objects.filter(is_open_public=True)

class ElectionResultViewSet(ReadOnlyModelViewSet):
    serializer_class = ElectionResultSerializer
    queryset = Election.objects.filter(is_open_public=True, results_out=True)

class CandidateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request, election_slug, slug, format=None):
        election = get_object_or_404(Election, slug=election_slug)
        candidate = get_object_or_404(Candidate, election=election, slug=slug)
        if not candidate.is_open_public:
            raise NotFound
        return Response(CandidateSerializer(candidate).data)
    
    def put(self, request, election_slug, slug, format=None):
        election = get_object_or_404(Election, slug=election_slug)
        candidate = get_object_or_404(Candidate, election=election, slug=slug)
        if candidate.account != request.user or election.start_datetime < datetime.datetime.now():
            raise PermissionDenied()
        serializer = CandidateSerializer(data=request.data)
        serializer.save()
        return Response()
    
@api_view(['GET', 'POST'])
@authentication_classes([IsKAuthenticated])
def vote_info(request):
    is_eligible = is_eligible(request.kaist_profile)
    already_voted = Vote.objects.filter(user=request.kaist_profile).exists()
    if request.method == 'GET':
        return Response({
            'is_eligible': is_eligible,
            'already_voted': already_voted
        })
    if request.method == 'POST':
        if not is_eligible:
            raise PermissionDenied(_("Sorry, you are not elligible for voting."))
        if already_voted:
            raise PermissionDenied(_("You have already voted."))
        result = Candidate.objects.filter(slug=request.data['candidate'])
        now = datetime.datetime.now()
        if (not result.exists()) or now < result[0].election.start_datetime or now > result[0].election.end_datetime:
            raise ParseError()
        if ElectionResultSerializer.get_election_type == 'multi':
            Vote(user=request.kaist_profile, candidate=result[0], vote_type=True).save()
        else:
            Vote(user=request.kaist_profile, candidate=result[0], vote_type=bool(request.data['vote_type']))
        return Response()
    
    raise MethodNotAllowed()

def is_eligible(user:KAISTProfile)->bool:
    if VotingExceptionToken.objects.filter(user=user, election=Election.objects.latest()).exists():
        return True
    if user.nationality == 'KOR' or user.kaist_email == None:
        return False
    if 'E' in user.user_group and 'researcher' in user.title_english.lower():
        return True
    return False
    