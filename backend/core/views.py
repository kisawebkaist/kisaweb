from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Footer, NavBar
from events.models import Event
from aboutus.models import DivisionContent
from django.conf import settings
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
import rest_framework.status as status

# Create your views here.

@ensure_csrf_cookie
def homepage(request):
    # if settings.MAINTENANCE_MODE == True:
    #     return redirect('important_links')
    # else:
    #     num_shown_events = 6
    #     events = Event.objects.all().order_by("-id")
    #     latest_events = events[: min(num_shown_events, len(events))]
    #     division_list = DivisionContent.objects.all()
    #     colors = ['red', 'green', 'orange', 'blue', 'black', 'purple']
    #     context = {
    #         "event_list": latest_events,
    #         "division_list": list(zip(division_list, colors)),
    #     }
    #     return render(request, 'core/homepage.html', context)
    return HttpResponse("Hi")

def important_links(request):
    return render(request, 'core/important_links.html')

@api_view(['GET'])
@ensure_csrf_cookie
def check_login_status_view(request):
    return JsonResponse({
        'member_logined': request.user.is_authenticated,
        'ksso_logined': request.kaist_profile.is_authenticated,
    })

class MiscAPIView(APIView):
    klass_from_endpoint = {
        'navbar': NavBar,
        'footer': Footer,
    }

    def get(self, request, format=None):
        for endpoint in MiscAPIView.klass_from_endpoint:
            if request.path == reverse('misc') + endpoint:
                klass = MiscAPIView.klass_from_endpoint[endpoint]
                serializer = klass.serializer_class(klass.get_deployed())
                return Response(serializer.data)
        return JsonResponse(status=status.HTTP_404_NOT_FOUND)