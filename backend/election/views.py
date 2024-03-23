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
from sso.permissions import IsKISAVerifiedOrReadOnly

from .models import Election, Candidate, Vote, VotingExceptionToken
from .serializers import *

# TODO: check this function with SSO documentation and the constitution
def is_eligible(user:User, election:Election)->bool:
    if election == None:
        election=Election.current_or_error()
    if VotingExceptionToken.objects.filter(user=user, election=election).exists() or user.is_kisa():
        return True
    if user.nationality == 'KOR' or user.kaist_email == None:
        return False
    # TODO: check what's happening here with old code
    if 'E' in user.employee_type and 'researcher' in user.title_english.lower():
        return True
    return True

class ElectionInfoViewSet(ReadOnlyModelViewSet):
    serializer_class = ElectionInfoSerializer
    queryset = Election.objects.filter(is_open_public=True).all()
    lookup_field = 'slug'

class ElectionResultViewSet(ReadOnlyModelViewSet):
    serializer_class = ElectionResultSerializer
    queryset = Election.objects.filter(is_open_public=True, results_out=True).all()
    lookup_field = 'slug'

class CandidateAPIView(APIView):
    permission_classes = [IsKISAVerifiedOrReadOnly]
    
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
        return Response({})
    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def vote(request):
    election = Election.current_or_error()
    eligible = is_eligible(request.user, election)
    already_voted = Vote.objects.filter(user=request.user, election=election).exists()

    if request.method == 'GET':
        return Response({
            'is_eligible': eligible,
            'already_voted': already_voted
        })
    if request.method == 'POST':
        candidate = Candidate.objects.filter(slug=request.data.get('candidate', ''), election=election).first()
        if candidate == None:
            raise ParseError()
        
        with transaction.atomic():
            if not eligible:
                raise PermissionDenied(_("Sorry, you are not elligible for voting."))
            if already_voted:
                raise PermissionDenied(_("You have already voted."))
            
            # if there's a race condition where two requests trigger save the 
            if election.get_election_type() == 'multi':
                Vote(user=request.user, election=election, candidate=candidate, vote_type=True).save()
            else:
                Vote(user=request.user, election=election, candidate=candidate, vote_type=bool(request.data['vote_type'])).save()
            return Response({})
    
    raise MethodNotAllowed(request.method)
    