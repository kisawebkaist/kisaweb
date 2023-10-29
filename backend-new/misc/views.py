from django.shortcuts import render
from misc.models import NavBarEntry
from misc.lib import *
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

class NavBarViewSet(ViewSet):
    def list(self, request):
        queryset = NavBarEntry.objects.all()
        for entry in queryset:
            entry.init_custom_fields()
        entries = [NavEntrySerializer(query).data for query in queryset]
        return Response(entries)
