from rest_framework import serializers
from .models import SportEvent, Sport, Season, SportLeague

class SportEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = SportEvent
        fields = '_all__'
        read_only_fields = ['id']
        depth = 2

    @staticmethod
    def get_league(obj):
        league = obj.league
        return f"hi, my league is {league}"

class SportListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sport
        fields = '__all__'
        read_only_fields = ['id']

class SportLeagueSerializer(serializers.ModelSerializer):

    class Meta:
        model = SportLeague
        fields = '__all__'
        read_only_fields = ['id']

class SeasonListSerializer(serializers.ModelSerializer):
    league = SportLeagueSerializer(read_only=True)

    class Meta:
        model = Season
        fields = '__all__'
        read_only_fields = ['id']