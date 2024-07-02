from rest_framework import serializers
from django.db.models import Q

from tournament.models import PoolEntry, Tournament
from sport.models import SportEvent
from tournament.serializers.player_sport_event import PlayerSportEventSerializer


class PoolEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = PoolEntry
        fields = '__all__'
        extra_kwargs = {'created_by': {'read_only': True}}
        depth = 1
        

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
            q_objects = Q(my_event__pool_entry__player=self.context.user)
            tournament_id = self.context.query_params.get('tournament_id')
            if tournament_id:
                q_objects &= Q(my_event__pool_entry__tournament__id=int(tournament_id))
            data = PlayerSportEventSerializer(SportEvent.objects.filter(q_objects), many=True, context=self.context).data
        return data