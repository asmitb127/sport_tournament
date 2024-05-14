from rest_framework import serializers

from choices.choice import Tournament_Type
from tournament.models import Tournament, PoolEntry, Picks
from sport.models import Sport, SportEvent, Season

from datetime import datetime


class TournamentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tournament
        fields = '__all__'
        extra_kwargs = {'creator': {'read_only': True}}
        depth = 1

    def validate_start_time(self, value):
        if value < datetime.now().date():
            raise serializers.ValidationError("Start time cannot be in the past")
        return value

    def validate_entry_fee(self, value):
        if value <= 0:
            raise serializers.ValidationError("Entry fee cannot be negative")
        return value 

    def create(self, validated_data):
        tournament = Tournament.objects.create(
            tournament_id=validated_data['tournament_id'],
            start_time=validated_data['start_time'],
            end_time=validated_data['end_time'],
            season_id=validated_data['season_id'],
            entry_fee=validated_data['entry_fee'],
            creator=self.context['request'].user,
            tournament_type=validated_data['tournament_type'],
        )
        [tournament.sport_event.add(each_event) for each_event in validated_data['sport_event']]
        tournament.save()
        return tournament


class PoolEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = PoolEntry
        fields = '__all__'
        extra_kwargs = {'created_by': {'read_only': True}}


