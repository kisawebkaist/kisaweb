from django.shortcuts import render
from .models import Alumni
# Create your views here.


def alumni_view(request):
    alumni_people = Alumni.objects.order_by('-separated_year')
    context = {
        'people': alumni_people
    }
    return render(request,'alumni_people.html',context)