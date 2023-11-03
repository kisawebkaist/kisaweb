from rest_framework import viewsets
from rest.models import *

# Create your views here.
class NavBarViewSet(viewsets.ModelViewSet):
    queryset = NavBar.objects.all()
    serializer_class = NavBar.serializer_class

class FooterViewSet(viewsets.ModelViewSet):
    queryset = Footer.objects.all()
    serializer_class = Footer.serializer_class