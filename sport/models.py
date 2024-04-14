from django.db import models
from django.utils.timezone import now

from datetime import datetime

from choices.choice import Status

# Create your models here.

class Team(models.Model):
    title = models.CharField(max_length=125)

    def __str__(self) -> str:
        return self.title

class Sport(models.Model):
    title = models.CharField(max_length=125)

    def __str__(self) -> str:
        return self.title

class SportLeague(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=125)

    def __str__(self) -> str:
        return self.title

class SportEvent(models.Model):
    league = models.ForeignKey(SportLeague, on_delete=models.RESTRICT)
    start_datetime = models.DateTimeField(default=now())
    end_datetime = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=Status, default=Status['A'])

    def __str__(self) -> str:
        return f"{self.start_datetime.date()} {self.league.sport.title} {self.league.title}"

class SportEventResult(models.Model):
    sport_event = models.ForeignKey(SportEvent, on_delete=models.CASCADE)
    home = models.ForeignKey(Team, on_delete=models.RESTRICT)
    away = models.ForeignKey(Team, on_delete=models.RESTRICT, related_name='away')
    home_score = models.FloatField(default=0)
    away_score = models.FloatField(default=0)

    def __str__(self) -> str:
        title = f"{self.sport_event.league.sport.title} {self.sport_event.league.title}"
        title += f' {self.home}: {self.home_score} {self.away}: {self.away_score}'
        return title