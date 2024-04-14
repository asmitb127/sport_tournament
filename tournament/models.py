from django.db import models

# Create your models here.
from choices.choice import Tournament_Type
from sport.models import SportEvent, Sport
from core.models import CustomUser


class Tournament(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.RESTRICT)
    sport_event = models.OneToOneField(SportEvent, on_delete=models.RESTRICT)
    type = models.CharField(max_length=1, choices=Tournament_Type)
    created_at = models.DateTimeField(auto_now=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.RESTRICT)

    def __str__(self) -> str:
        title = f"{self.sport_event} {self.created_by}"
        return title

class TournamentPool(models.Model):
    pool = models.ForeignKey(Tournament, on_delete=models.RESTRICT)
    player = models.ForeignKey(CustomUser, on_delete=models.RESTRICT)

    def __str__(self):
        title = f'{Tournament_Type[self.pool.type]} {self.pool.sport_event} {self.player}'
        return title