from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.translation import gettext as _
from django.urls import reverse

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
import rest_framework.status as status

from .models import Footer, NavBar

# def important_links(request):
#     return render(request, 'core/important_links.html')

# TODO: Discuss with frontend devs for format
@api_view(['GET'])
@ensure_csrf_cookie
def get_state_view(request):
    """
    For Frontend
    ------------
    - Everytime the page loads, make a request to this endpoint to fetch the state information stored in backend.
    - This will also set the csrftoken cookie
    """
    return JsonResponse({
        'member_logined': request.user.is_authenticated,
        'ksso_logined': request.kaist_profile.is_authenticated,
    })

# TODO: poorly designed, rewrite
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