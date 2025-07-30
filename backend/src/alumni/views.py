from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Alumni
from .serializers import AlumniSerializer

@api_view(['GET'])
def alumni_api_view(request):
    alumni_people = Alumni.objects.order_by('-separated_year')
    serializer = AlumniSerializer(alumni_people, many=True)
    return Response(serializer.data)