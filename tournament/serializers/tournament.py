from rest_framework import serializers

from choices.choice import Tournament_Type
from tournament.models import Tournament, PoolEntry, Picks
from sport.models import Sport, SportEvent, Season


from datetime import datetime


class TournamentListSerializer(serializers.ModelSerializer):
    player_count = serializers.IntegerField()
    class Meta:
        model = Tournament
        fields = '__all__'
        extra_kwargs = {'creator': {'read_only': True}}
        depth = 2


class TournamentSerializer(serializers.ModelSerializer):
    season = serializers.PrimaryKeyRelatedField(
        queryset=Season.objects.all()
    )
    sport_event = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=SportEvent.objects.all()
    )

    class Meta:
        model = Tournament
        fields = '__all__'
        extra_kwargs = {'creator': {'read_only': True}}
        depth = 1

    def validate_season(self, value):
        return value

    def validate_start_time(self, value):
        if value < datetime.now().date():
            raise serializers.ValidationError("Start time cannot be in the past")
        return value

    def validate_entry_fee(self, value):
        if value <= 0:
            raise serializers.ValidationError("Entry fee cannot be negative")
        return value

    def validate(self, attrs):
        if not attrs.get('sport_event'):
            raise serializers.ValidationError({'sport_event': ['This field is required.']})
        return super().validate(attrs)

    def create(self, validated_data):
        tournament = Tournament.objects.create(
            tournament_id= validated_data['tournament_id'],
            name= validated_data['name'],
            start_time= validated_data['start_time'],
            end_time= validated_data['end_time'],
            season= validated_data['season'],
            entry_fee= validated_data['entry_fee'],
            creator= self.context['request'].user,
            tournament_type= validated_data['tournament_type'],
            sport = validated_data['season'].league.sport
        )
        [tournament.sport_event.add(each_event) for each_event in validated_data['sport_event']]
        tournament.save()
        return tournament



