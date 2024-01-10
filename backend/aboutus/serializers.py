import rest_framework.serializers as serializer
from .models import \
    DivisionContent, \
    Member, \
    InternalBoardMember

class DivisionSerializer(serializer.ModelSerializer):
    class Meta:
        model = DivisionContent
        fields = [
            'division_name', 'id'
        ]

class MemberSerializer(serializer.ModelSerializer):
    division = serializer.PrimaryKeyRelatedField(read_only = True)
    class Meta:
        model = Member
        fields = [
            'name',
            'image',
            'year',
            'semester',
            'sns_link',
            'division'
        ]

class InternalBoardMemberSerializer(serializer.ModelSerializer):
    division = serializer.PrimaryKeyRelatedField(read_only = True)
    class Meta:
        model = InternalBoardMember
        fields = [
            'name',
            'image',
            'year',
            'semester',
            'sns_link',
            'position',
            'division'
        ]
