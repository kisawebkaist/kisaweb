import rest_framework.serializers as serializers

from .models import Candidate, Election, Vote

class CandidateSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    election = serializers.SerializerMethodField()
    manifesto = serializers.JSONField()
    speech_url = serializers.URLField(required=False)
    kisa_history = serializers.JSONField(required=False)
    image = serializers.ImageField(required=False)
    slug = serializers.SlugField()

    class Meta:
        model = Candidate
        fields = ['manifesto', 'speech_url', 'kisa_history', 'image']

    def get_name(self, candidate):
        return candidate.account.get_full_name()
    
    def get_election(self, candidate):
        return candidate.election.slug
    

class ElectionInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Election
        fields = [
            'start_datetime',
            'end_datetime',
            'intro_msg',
            'instructions',
            'image',
            'debate_url',
            'slug',
            'candidates'
        ]
    start_datetime = serializers.DateTimeField()
    end_datetime = serializers.DateTimeField()
    intro_msg = serializers.JSONField()
    instructions = serializers.JSONField()
    image = serializers.ImageField()
    debate_url = serializers.URLField()
    slug = serializers.SlugField()
    candidates = serializers.SerializerMethodField()

    def get_candidates(self, election):
        return CandidateSerializer(Candidate.objects.filter(election=election), many=True).data
    
class ElectionResultSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            'slug'
        ]
    election_type = serializers.SerializerMethodField()
    result = serializers.SerializerMethodField()

    def get_election_type(self, election):
        return 'multi' if Candidate.objects.filter(election=election).count()>1 else 'single'
    
    def get_result(self, election):
        candidates = Candidate.objects.filter(election=election)
        if candidates.count() == 1:
            return {
                'yes': Vote.objects.filter(candidate=candidates[0], vote_type=True),
                'no': Vote.objects.filter(candidate=candidates[0], vote_type=False)
            }
        
        result = dict()
        for candidate in candidates:
            result[candidate.slug] = candidate.num_votes
        return result
    