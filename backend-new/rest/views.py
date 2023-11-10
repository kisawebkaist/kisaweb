from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest.models import *

# Create your views here.
class MiscAPIView(APIView):
    klass_from_endpoint = {
        'navbar': NavBar,
        'footer': Footer,
    }

    def get(self, request, format=None):
        for endpoint in MiscAPIView.klass_from_endpoint:
            if request.path.strip() == '/api/misc/'+endpoint:
                klass = MiscAPIView.klass_from_endpoint[endpoint]
                serializer = klass.serializer_class(klass.get_deployed())
                return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)