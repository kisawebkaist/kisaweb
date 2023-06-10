from django.shortcuts import render
from django.db.models import F
from datetime import datetime

from .models import MainContent, Member, InternalBoardMember, DivisionContent, ConstitutionPDF

def aboutus(request):
    current_date = datetime.today()
    year, semester = current_date.year, ('Fall' if current_date.month > 6 else 'Spring')
    
    internal_board_members = InternalBoardMember.objects.filter(year=year, semester=semester)
    members = Member.objects.filter(year=year, semester=semester)
    constitution     = ConstitutionPDF.objects.annotate(
        pdf_url = F('constitution_file')
    ).values(
        'title', 'desc', 'pdf_url'
    ).all()
    request_scheme = request.build_absolute_uri().split('://', 1)[0]
    context = {
        'main_contents'             : MainContent.objects.all(),
        'division_descriptions'     : DivisionContent.objects.all(),
        'internal_board_members'    : internal_board_members,
        'members'                   : members,
        'constitution'              : constitution,
        'request_scheme'            : request_scheme
    }
    return render(request, 'aboutus/aboutus.html', context)