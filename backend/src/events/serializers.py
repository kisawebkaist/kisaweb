from .models import Event
import rest_framework.serializers as serializers

class EventPartialSerializer(serializers.ModelSerializer):
    current_occupancy = serializers.SerializerMethodField()
    class Meta:
        model = Event
        exclude = [
            'id',
            'description',
            'participants'
        ]
        include = [
            'current_occupancy'
        ]
    def get_current_occupancy(self, obj):
        return len(obj.participants.all())

class EventSerializer(serializers.ModelSerializer):
    current_occupancy = serializers.SerializerMethodField()
    class Meta:
        model = Event
        exclude = [
            'id',
            'participants'
        ]
        include = [
            'current_occupancy'
        ]
    def get_current_occupancy(self, obj):
        return len(obj.participants.all())