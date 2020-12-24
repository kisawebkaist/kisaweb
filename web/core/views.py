from django.shortcuts import render, HttpResponse


# Create your views here.

def homepage(request):
    return redirect('election')


def course_resources(request):
    resources = CourseResources.objects.order_by('class_id')
    return render(request, 'core/course_resources.html', context={
        'resources': resources,
    })
