from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.translation import gettext as _

from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .models import Misc

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
    return Response({
        'member_logined': request.user.is_authenticated,
        'ksso_logined': request.kaist_profile.is_authenticated,
    })


@api_view(['GET'])
def get_misc_view(request, slug=""):
    query = Misc.objects.filter(slug=slug)
    if query.exists() and query[0].is_active:
        return JsonResponse(
            query[0].data,
            safe=False
        )
    raise NotFound()