import rest_framework.serializers as serializer

from core.serializers import SemesterSerailizer
from .models import *

class KISADivisionContentSerializer(serializer.ModelSerializer):
    class Meta:
        model = KISADivisionContent
        fields = [
            'division', 
            'content',
        ]

    
class KISARoleSerializer(serializer.ModelSerializer):
    semester = SemesterSerailizer
    class Meta:
        model = KISARole
        fields = [
            'semester', 
            'division', 
            'is_head',
        ]

class KISAMemberSerializer(serializer.ModelSerializer):
    name = serializer.SerializerMethodField()
    department = serializer.SerializerMethodField()
    exp = serializer.SerializerMethodField()
    class Meta:
        model = KISAMember
        fields = [
            'name',
            'department',
            'exp',
            'image',
            'sns_link',
        ]
    
    def get_name(self, obj):
        return obj.user.get_full_name()
    
    def get_department(self, obj):
        return obj.user.student_department_name_english or obj.user.student_department_name_english or ''
    
    def get_exp(self, obj):
        return KISARoleSerializer(KISARole.objects.filter(members=obj).all(), many=True).data
