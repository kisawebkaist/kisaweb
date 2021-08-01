from django.shortcuts import render, HttpResponse, redirect

from .models import Main, Members, Division, Board

def aboutus(request):
    main    = list(Main.objects.all())
    member  = list(Members.objects.all())
    division= list(Division.objects.all())
    board   = list(Board.objects.all())
    context = {
        "main"      : main, 
        "member"    : member, 
        "division"  : division,
        "board"     : board
    }
    return render(request, 'aboutus/aboutus.html', context)