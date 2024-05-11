from rest_framework import serializers
from .models import SportEvent, Sport

class SportEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = SportEvent
        fields = ['event_id', 'league', 'home_team', 'away_team', 
                  'start_datetime', 'status', 'home_score', 'away_score']
        read_only_fields = ['id']

    @staticmethod
    def get_league(obj):
        league = obj.league
        return f"hi, my league is {league}"

class SportListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sport
        fields = '__all__'
        read_only_fields = ['id']