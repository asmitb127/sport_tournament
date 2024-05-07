from rest_framework import serializers

from choices.choice import Tournament_Type
from tournament.models import Tournament, TournamentPool
from sport.models import Sport, SportEvent


class TournamentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tournament
        fields = '__all__'
        extra_kwargs = {'created_by': {'read_only': True}}


    def create(self, validated_data):
        sport_id = validated_data['sport']
        try:
            sport = Sport.objects.get(pk=sport_id)
        except Sport.DoesNotExist:
            raise Exception({'sport': ['Sport not found']})
        sport_event_id = validated_data['sport_event']
        try:
            sport_event = SportEvent.objects.get(pk=sport_event_id)
        except Sport.DoesNotExist:
            raise Exception({'sport': ['Sport not found']})
        if not validated_data['type'] in Tournament_Type.values():
            raise Exception({'type': ['Wrong type entered.']})

        tournament = Tournament.objects.create(
            sport=sport,
            sport_event=sport_event,
            type=validated_data['type'],
            start_date=validated_data['start_date'],
            end_date=validated_data['end_date'],
            created_by=self.created_by
        )

        tournament.save()
        return tournament

