import datetime

from django.db import transaction
from django.utils.translation import gettext as _

from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import MethodNotAllowed, NotFound, PermissionDenied, ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from core.utils import get_object_or_404
from sso.models import User
from sso.permissions import IsKISA, IsVerifiedOrReadOnly

from .models import Election, Candidate, Vote, VotingExceptionToken
from .serializers import *

ELIGIBLE_USER_TYPES = "SGR" # students, graduates, researchers

def is_eligible(user:User, election:Election)->bool:
    '''See `Article.I.A.2` of KISA Constitution'''
    if election == None:
        election=Election.current_or_error()

    if VotingExceptionToken.objects.filter(user=user, election=election).exists() or user.is_kisa():
        return True
    
    if user.nationality == 'KOR':
        return False
    for flag in ELIGIBLE_USER_TYPES:
        if flag in user.employee_type:
            return True
    
    return False

class ElectionInfoViewSet(ReadOnlyModelViewSet):
    serializer_class = ElectionInfoSerializer
    queryset = Election.objects.filter(is_open_public=True).all()
    lookup_field = 'slug'

class ElectionResultViewSet(ReadOnlyModelViewSet):
    serializer_class = ElectionResultSerializer
    queryset = Election.objects.filter(is_open_public=True, results_out=True).all()
    lookup_field = 'slug'

class CandidateAPIView(APIView):
    permission_classes = [IsKISA, IsVerifiedOrReadOnly]
    
    def get(self, request, election_slug, slug, format=None):
        election = get_object_or_404(Election, slug=election_slug)
        candidate = get_object_or_404(Candidate, election=election, slug=slug)
        if not candidate.is_open_public:
            raise NotFound
        return Response(CandidateSerializer(candidate).data)
    
    # def put(self, request, election_slug, slug, format=None):
    #     election = get_object_or_404(Election, slug=election_slug)
    #     candidate = get_object_or_404(Candidate, election=election, slug=slug)
    #     if candidate.account != request.user or election.start_datetime < datetime.datetime.now():
    #         raise PermissionDenied()
    #     serializer = CandidateSerializer(data=request.data)
    #     serializer.save()
    #     return Response({})
    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def vote(request):
    election = Election.current_or_error()
    eligible = is_eligible(request.user, election)

    if request.method == 'GET':
        return Response({
            'is_eligible': eligible,
            'already_voted': Vote.objects.filter(user=request.user, election=election).exists()
        })
    
    if request.method == 'POST':
        candidate = Candidate.objects.filter(slug=request.data.get('candidate', ''), election=election).first()
        if candidate == None or request.data.get('vote_type') == None:
            raise ParseError()
        
        with transaction.atomic():
            if not eligible:
                raise PermissionDenied(_("Sorry, you are not elligible for voting."))
            
            vote_type = bool(request.data['vote_type'])
            if election.get_election_type() == 'multi':
                vote_type = True
            
            vote, created = Vote.objects.select_for_update(nowait=True).get_or_create(user=request.user, election=election)
            if not created:
                raise PermissionDenied(_('You have already voted.'))
            vote.candidate = candidate
            vote.vote_type = vote_type
            return Response({})
    
    raise MethodNotAllowed(request.method)

# Check Election Period API
class ElectionStatusAPIView(APIView):
    def get(self, request):
        try:
            election = Election.current_or_error()
            return Response({
                "status": "ongoing",
                "election": {
                    "start_datetime": election.start_datetime,
                    "end_datetime": election.end_datetime,
                    "slug": election.slug
                }
            })
        except ParseError:
            return Response({"status": "none"})