from rest.utils import JSONModel, JSONModelSerializer

class NavBar(JSONModel):
    schema_title="NavBarT"
    deployed_pk = 1

class Footer(JSONModel):
    schema_title = "Footer"
    deployed_pk = 1

class NavBarSerializer(JSONModelSerializer):
    model_class = NavBar

class FooterSerializer(JSONModelSerializer):
    model_class = Footer