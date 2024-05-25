from rest_framework import serializers

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
            data = PicksSerializer(Picks.objects.filter(id__in=obj.my_event.values_list('id', flat=True), pool_entry__player=self.context.user), many=True).data
        return data

