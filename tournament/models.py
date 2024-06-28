from django.db import models
from django.utils.timezone import now

from choices.choice import NETWORK, Tournament_Type, PICK_CHOICE
from sport.models import Season, SportEvent, SportLeague, Sport
from core.models import CustomUser


class Tournament(models.Model):
    '''
    Pool is tournament.
    '''

    name = models.CharField(max_length=255)
    tournament_id = models.CharField(max_length=255, unique=True)
    start_time = models.DateField()
    end_time = models.DateField()
    league = models.ForeignKey(SportLeague, on_delete=models.RESTRICT)
    # season = models.ForeignKey(Season, on_delete=models.RESTRICT)
    entry_fee = models.FloatField()
    creator = models.ForeignKey(CustomUser, on_delete=models.RESTRICT)
    tournament_type = models.CharField(max_length=10, choices=Tournament_Type, default=Tournament_Type['O'])
    sport_event = models.ManyToManyField(SportEvent, related_name='tournament')
    sport = models.ForeignKey(Sport, blank=True, null=True, on_delete=models.RESTRICT)

    def __str__(self) -> str:
        title = f"{self.name} {self.creator}"
        return title

class PoolEntry(models.Model):
    '''
    User Joins Tournament.
    '''
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE,related_name='my_pool_entry')
    entry_txn = models.TextField(max_length=100)
    player = models.ForeignKey(CustomUser, on_delete=models.RESTRICT, related_name='my_pool')
    network = models.CharField(max_length=10, choices=NETWORK,default=NETWORK['ETH'] )
    join_time = models.DateTimeField(default=now())


class Picks(models.Model):
    pool_entry = models.ForeignKey(PoolEntry, on_delete=models.CASCADE, related_name='my_picks')
    event_id = models.ForeignKey(SportEvent, on_delete=models.CASCADE, related_name='my_event')
    pick = models.CharField(max_length=5, choices=PICK_CHOICE)

