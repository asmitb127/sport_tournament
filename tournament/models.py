from django.db import models
from django.utils.timezone import now

# Create your models here.
from choices.choice import NETWORK, Tournament_Type, PICK_CHOICE
from sport.models import SportEvent, Sport
from core.models import CustomUser

from sport.models import Season, SportEvent
from core.models import CustomUser

# pool is tournament 
class Tournament(models.Model):

    name = models.CharField(max_length=255)
    tournament_id = models.CharField(max_length=255, unique=True)
    start_time = models.DateField()
    end_time = models.DateField()
    season = models.ForeignKey(Season, on_delete=models.RESTRICT)
    entry_fee = models.FloatField()
    creator = models.ForeignKey(CustomUser, on_delete=models.RESTRICT)
    tournament_type = models.CharField(max_length=10, choices=Tournament_Type, default=Tournament_Type['O'])
    sport_event = models.ManyToManyField(SportEvent)

    def __str__(self) -> str:
        title = f"{self.sport_event} {self.created_by}"
        return title
    
# it saves the pool entry for the tournament for different users 
class PoolEntry(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    entry_txn = models.TextField(max_length=100)
    player = models.ForeignKey(CustomUser, on_delete=models.RESTRICT)
    network = models.CharField(max_length=10, choices=NETWORK,default=NETWORK['ETH'] )
    join_time = models.DateTimeField(default=now())

    
class Picks(models.Model):
    pool_entry = models.ForeignKey(PoolEntry, on_delete=models.CASCADE)
    event_id = models.ForeignKey(SportEvent, on_delete=models.CASCADE)
    pick = models.CharField(max_length=5, choices=PICK_CHOICE)

