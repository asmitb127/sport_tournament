from datetime import datetime

from rest_framework import serializers
from django.db.models import Case, When, Value, F, CharField

from tournament.models import PoolEntry, Tournament
from tournament.serializers.pick import PicksSerializer

from helper.utils import get_week_from_date


class LeaderboardSerializer(serializers.ModelSerializer):
    points = serializers.IntegerField()
    week = serializers.IntegerField()
    strike_rate = serializers.IntegerField()
    rank = serializers.IntegerField()

    class Meta:
        model = Tournament
        fields = ['name', 'points', 'week', 'strike_rate', 'rank']

    def get_fields(self):
        fields = super().get_fields()
        fields['points'] = serializers.SerializerMethodField()
        fields['week'] = serializers.SerializerMethodField()
        fields['strike_rate'] = serializers.SerializerMethodField()
        fields['rank'] = serializers.SerializerMethodField()
        return fields

    def get_points(self, obj):
        pool_entry_with_winner = PoolEntry.objects.filter(
                                    player=self.context.user,
                                    my_picks__event_id__status='active',
                                    tournament__end_time__gte=datetime.now().date()
                                ).annotate(
                                    winner=Case(
                                        When(my_picks__event_id__home_score__gt=F('my_picks__event_id__away_score'), then=Value('home')),
                                        When(my_picks__event_id__home_score__lt=F('my_picks__event_id__away_score'), then=Value('away')),
                                        default=Value('draw'),
                                        output_field=CharField()
                                    ),
                                )
        data = pool_entry_with_winner.filter(winner=F('my_picks__pick')).count()
        return data

    def get_week(self, obj):
        return get_week_from_date(obj.start_time, obj.end_time)

    def get_strike_rate(self, obj):
        return '75%'

    def get_rank(self, obj):
        return 0

