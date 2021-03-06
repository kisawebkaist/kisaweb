from django.shortcuts import render, HttpResponse, redirect
from events.models import Event
from django.conf import settings

from .models import CourseResources

# Create your views here.

def homepage(request):
    if settings.MAINTENANCE_MODE == True:
        return redirect('important_links')
    else:
        num_shown_events = 6
        events = Event.objects.all().order_by("-id")
        latest_events = events[: min(num_shown_events, len(events))]
        context = {
            "event_list": latest_events
        }
        return render(request, 'core/homepage.html', context)

def important_links(request):
    return render(request, 'core/important_links.html')

def course_resources(request):
    resources = CourseResources.objects.order_by('class_id')
    return render(request, 'core/course_resources.html', context={
        'resources': resources,
    })
