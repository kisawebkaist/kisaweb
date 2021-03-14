from django.shortcuts import render, HttpResponse, redirect
from django.conf import settings

from .models import CourseResources

# Create your views here.

def homepage(request):
    if settings.MAINTENANCE_MODE == True:
        return redirect('important_links')
    else:
        return redirect('events')

def important_links(request):
    return render(request, 'core/important_links.html')

def course_resources(request):
    resources = CourseResources.objects.order_by('class_id')
    return render(request, 'core/course_resources.html', context={
        'resources': resources,
    })
