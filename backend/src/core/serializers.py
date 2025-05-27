from rest_framework import serializers

from .models import Semester

class SemesterSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['year', 'season']