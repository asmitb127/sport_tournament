from rest_framework import serializers

from tournament.models import PoolEntry, Tournament
from sport.models import SportEvent
from tournament.serializers.player_sport_event import PlayerSportEventSerializer


class PoolEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = PoolEntry
        fields = '__all__'
        extra_kwargs = {'created_by': {'read_only': True}}

class PoolEntryEventSerializer(serializers.ModelSerializer):
    sport_event = serializers.PrimaryKeyRelatedField(
        queryset=SportEvent.objects.all()
    )

    class Meta:
        model = Tournament
        fields = '__all__'

    def get_fields(self):
        fields=super().get_fields()
        fields['sport_event'] = serializers.SerializerMethodField()
        return fields

    def get_sport_event(self, obj):
        data = None
        if obj.sport_event:
            data = PlayerSportEventSerializer(SportEvent.objects.filter(my_event__pool_entry__player=self.context.user), many=True, context=self.context).data
        return data