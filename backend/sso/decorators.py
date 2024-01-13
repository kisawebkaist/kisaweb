from functools import wraps

from django.utils.translation import gettext as _

from rest_framework.exceptions import PermissionDenied

def klogin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.kaist_profile.is_authenticated:
            raise PermissionDenied(detail=_("You need to login with KAIST account for this request."))
        return view_func(request, *args, **kwargs)
    return _wrapped_view