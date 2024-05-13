from rest_framework import serializers

from choices.choice import Tournament_Type
from tournament.models import Tournament, PoolEntry, Picks
from sport.models import Sport, SportEvent

from datetime import datetime


class TournamentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tournament
        fields = '__all__'
        extra_kwargs = {'created_by': {'read_only': True}}

    def validate_start_time(self, value):
        if value < datetime.now():
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
            sport_event=validated_data['sport_event']
        )

        #save the data
        tournament.save()
        return tournament


class PoolEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = PoolEntry
        fields = '__all__'
        extra_kwargs = {'created_by': {'read_only': True}}


