from django.shortcuts import render

from .models import Main, Members, Division, Board

def aboutus(request):
    context = {
        "main"      : Main.objects.all(), 
        "member"    : Members.objects.all(), 
        "division"  : Division.objects.all(),
        "board"     : Board.objects.all()
    }
    return render(request, 'aboutus/aboutus.html', context)