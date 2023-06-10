from django.shortcuts import render
from django.db.models import F
from datetime import datetime

from .models import MainContent, Member, InternalBoardMember, DivisionContent, ConstitutionPDF

def aboutus(request):
    current_date = datetime.today()
    year, semester = current_date.year, ('Fall' if current_date.month > 6 else 'Spring')
    
    internal_board_members = InternalBoardMember.objects.filter(year=year, semester=semester)
    members = Member.objects.filter(year=year, semester=semester)
    if request.is_secure():
        request_scheme = 'https'
    elif 'X-Forwarded-Proto' in request.META:
        request_scheme = request.META['X-Forwarded-Proto']
    else:
        request_scheme = request.scheme
    constitution     = ConstitutionPDF.objects.annotate(
        pdf_url = F('constitution_file')
    ).values(
        'title', 'desc', 'pdf_url'
    ).all()
    context = {
        'main_contents'             : MainContent.objects.all(),
        'division_descriptions'     : DivisionContent.objects.all(),
        'internal_board_members'    : internal_board_members,
        'members'                   : members,
        'constitution'              : constitution,
        'request_scheme'            : request_scheme
    }
    return render(request, 'aboutus/aboutus.html', context)