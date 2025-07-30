from rest_framework import serializers
from .models import Alumni, KISA_Position

class KISA_PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = KISA_Position
        fields = ['name']

class AlumniSerializer(serializers.ModelSerializer):
    worked_positions = KISA_PositionSerializer(many=True)

    class Meta:
        model = Alumni
        fields = ['name', 'joined_season', 'joined_year', 'separated_season', 'separated_year', 'worked_positions', 'current_contact']
