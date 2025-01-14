from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException
import rest_framework.status as status

class IncorrectEndpointException(APIException):
    status_code = status.HTTP_418_IM_A_TEAPOT
    default_detail = _('Yep, I\'m not a coffee pot.')
    default_code = 'incorrect_endpoint'