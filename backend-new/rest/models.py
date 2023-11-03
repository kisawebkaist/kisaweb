from rest.utils import JSONModel
from rest.serializers import *

class NavBar(JSONModel):
    schema_title="NavBarT"
    serializer_class=NavBarSerializer

class Footer(JSONModel):
    schema_title = "Footer"
    serializer_class=FooterSerializer
