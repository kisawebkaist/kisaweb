import enum

from misc.models import NavLinkData, NavDropdownData
from rest_framework import serializers

class NavEntryDataField(serializers.Field):
    '''
    A serializer field for data of NavEntry
    '''
    def to_representation(self, value):
        type = NavEntryType.get_type_from_data(value)
        return type.value[2](value).data
    
    def to_internal_value(self, data):
        type = NavEntryType.get_type_from_data(data)
        serializer = type.value[2](data=data)
        if serializer.is_valid():
            return serializer.validated_data
        else:
            raise serializers.ValidationError("Failed deserializing NavEntryDataField")
    
class NavLinkDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = NavLinkData
        fields = ['href', 'text', 'style']
    
    def to_representation(self, instance):
        result = super().to_representation(instance)
        if result['style'] == '':
            result.pop('style')
        return result

class NavDropdownDataSerializer(serializers.ModelSerializer):
    entries = NavLinkDataSerializer(read_only=True, many=True)
    class Meta:
        model = NavDropdownData
        fields = ['display', 'entries']

class NavEntrySerializer(serializers.Serializer):
    type = serializers.CharField(max_length=20)
    data = NavEntryDataField()

class NavEntryType(enum.Enum):
    """
    Enum that stores all informations related to each NavEntry type as tuple.
    It contains the following information in this order.

    0. string representation
    1. data class
    2. data serializer class
    """
    LINK = ('link', NavLinkData, NavLinkDataSerializer)
    DROPDOWN = ('dropdown', NavDropdownData, NavDropdownDataSerializer)
    @classmethod
    def get_type_from_data(cls, obj):
        for type in NavEntryType:
            if isinstance(obj, type.value[1]):
                return type
        return None
    