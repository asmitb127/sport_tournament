from rest_framework import serializers

from tournament.models import Picks


class PicksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Picks
        fields = '__all__'