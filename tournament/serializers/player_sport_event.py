from rest_framework import serializers
from django.db.models import Q, F

from sport.models import SportEvent
from tournament.models import Picks

from tournament.serializers.pick import PicksSerializer


class PlayerSportEventSerializer(serializers.ModelSerializer):
    my_event = serializers.PrimaryKeyRelatedField(
        queryset = Picks.objects.all()
    )

    class Meta:
        model = SportEvent
        fields = '__all__'

    def get_fields(self):
        fields = super().get_fields()
        fields['my_event'] = serializers.SerializerMethodField()
        return fields

    def get_my_event(self, obj):
        data = None
        if obj.my_event:
            q_objects = Q(id__in=obj.my_event.values_list('id', flat=True)) &  Q(pool_entry__player=self.context.user)
            tournament_id = self.context.query_params.get('tournament_id')
            if tournament_id:
                q_objects &= Q(pool_entry__tournament__id=int(tournament_id)) & Q(event_id=obj)
                data = PicksSerializer(Picks.objects.filter(q_objects).first()).data
        return data

