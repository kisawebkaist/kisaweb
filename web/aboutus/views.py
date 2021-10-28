from django.shortcuts import render
from datetime import datetime

from .models import MainContent, Member, InternalBoardMember, DivisionDescription

def aboutus(request):
    current_date = datetime.today()
    year, semester = current_date.year, ('Fall' if current_date.month > 6 else 'Spring')
    
    internal_board_members = InternalBoardMember.objects.filter(year=year, semester=semester)
    members = Member.objects.filter(year=year, semester=semester)

    context = {
        'main_contents'             : MainContent.objects.all(),
        'division_descriptions'     : DivisionDescription.objects.all(),
        'internal_board_members'    : internal_board_members,
        'members'                   : members,
    }
    return render(request, 'aboutus/aboutus.html', context)