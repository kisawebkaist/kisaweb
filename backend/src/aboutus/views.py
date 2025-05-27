from django.shortcuts import get_object_or_404

from rest_framework import generics, viewsets, parsers, permissions

from core.models import Semester
from .serializers import *

class CurrentKISAMemberListView(generics.ListAPIView):
    serializer_class = KISAMemberSerializer
    
    def get_queryset(self):
        semester = Semester.get_latest_nonbreak_semester()
        if semester is None:
            raise Exception("Latest non-break semester can't be None")
        queryset = KISAMember.objects.filter(kisarole__semester=semester).distinct()
        
        division = self.request.query_params.get('division')
        is_head = self.request.query_params.get('is_head')
        if division is not None:
            queryset = queryset.filter(kisarole__division=int(division))
        if is_head is not None:
            queryset = queryset.filter(kisarole__is_head=(is_head.lower()=='true'))
        
        return queryset
    
class KISADivisionContentViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = KISADivisionContentSerializer
    queryset = KISADivisionContent.objects.all()

class MyKISAMemberView(generics.RetrieveUpdateAPIView):
    serializer_class = KISAMemberSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def get_object(self):
        return get_object_or_404(KISAMember, user=self.request.user)