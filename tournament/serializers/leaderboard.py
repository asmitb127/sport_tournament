from datetime import datetime

from rest_framework import serializers
from django.db.models import Case, When, Value, F, CharField, Count, Min

from core.models import CustomUser
from core.serializers import UserInfoSerializer
from tournament.models import PoolEntry, Tournament
from tournament.serializers.pick import PicksSerializer

from helper.utils import get_week_from_date


class PlayerPointSerializer(serializers.ModelSerializer):
    player= serializers.PrimaryKeyRelatedField(
        queryset = CustomUser.objects.all()
    )
    points= serializers.IntegerField()

    class Meta:
        model = PoolEntry
        fields = ['player', 'points']

    def get_fields(self):
        fields = super().get_fields()
        fields['player'] = serializers.SerializerMethodField()
        fields['points'] = serializers.SerializerMethodField()
        return fields

    def get_points(self, obj):
        return obj.points
    
    def get_player(self, obj):
        return UserInfoSerializer(obj.player).data


class LeaderboardSerializer(serializers.ModelSerializer):
    points = serializers.IntegerField()
    week = serializers.IntegerField()
    strike_rate = serializers.IntegerField()
    rank = serializers.IntegerField()
    leaderboard = serializers.JSONField()

    class Meta:
        model = Tournament
        fields = ['name', 'points', 'week', 'strike_rate', 'rank', 'leaderboard']

    def get_fields(self):
        fields = super().get_fields()
        fields['points'] = serializers.SerializerMethodField()
        fields['week'] = serializers.SerializerMethodField()
        fields['strike_rate'] = serializers.SerializerMethodField()
        fields['rank'] = serializers.SerializerMethodField()
        fields['leaderboard'] = serializers.SerializerMethodField()
        return fields

    def get_points(self, obj):
        pool_entry_with_winner = PoolEntry.objects.filter(
                                    player=self.context.user,
                                    tournament=obj
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

    def get_leaderboard(self, obj):
        '''
        Tournament with all player joined with order by point desc.
        '''
        pool_entry_with_winners = PoolEntry.objects.filter(
                            tournament=obj
                        ).annotate(
                            winner=Case(
                                When(my_picks__event_id__home_score__gt=F('my_picks__event_id__away_score'), then=Value('home')),
                                When(my_picks__event_id__home_score__lt=F('my_picks__event_id__away_score'), then=Value('away')),
                                default=Value('draw'),
                                output_field=CharField()
                            ),
                        )
        data= PlayerPointSerializer(pool_entry_with_winners.filter(winner=F('my_picks__pick')).annotate(points=Count('player_id')).order_by('player_id'), many=True).data
        datab = PlayerPointSerializer(pool_entry_with_winners.exclude(winner=F('my_picks__pick')).annotate(points=Min(0)).order_by('player_id'), many=True).data
        return data+datab
