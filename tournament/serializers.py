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
            # tournament_id=validated_data['tournament_id'],
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

    def validate_join_time(self, value):
        if value < datetime.now():
            raise serializers.ValidationError("Join time cannot be in the past")
        return value

    def validate_picks(self, value):
        for pick in value:
            if not SportEvent.objects.filter(event_id=pick['event_id']).exists():
                raise serializers.ValidationError("Sport event does not exist")
        return value

    def create(self, validated_data):
        tournament_id = validated_data['tournament_id']
        if not Tournament.objects.filter(tournament_id=tournament_id).exists():
            raise serializers.ValidationError("Tournament does not exist")

        pool_entry = PoolEntry.objects.create(
            tournament=Tournament.objects.get(tournament_id=tournament_id),
            entry_txn=validated_data['entry_txn'],
            network=validated_data['network'],
            join_time=validated_data['join_time']
        )
        pool_entry.save()

        for pick in validated_data['picks']:
            sport_event = SportEvent.objects.get(event_id=pick['event_id'])
            Picks.objects.create(
                pool_entry=pool_entry,
                event_id=sport_event,
                pick=pick['pick']
            ).save()

        return pool_entry

