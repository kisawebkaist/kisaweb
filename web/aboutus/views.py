from django.shortcuts import render
from django.http import HttpResponse

from .models import MainContent, Member, InternalBoardMember, DivisionDescription

def aboutus(request):
    context = {
        'main_contents'             : MainContent.objects.all(),
        'internal_board_members'    : InternalBoardMember.objects.all(),
        'members'                   : Member.objects.all(),
        'division_descriptions'     : DivisionDescription.objects.all(),
    }
    return render(request, 'aboutus/aboutus.html', context)