from django.db import models
from django.utils.timezone import now

from datetime import datetime

from choices.choice import Sport_Status


# Sport saves the type of sport 
class Sport(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=125)

    def __str__(self) -> str:
        return self.title

# Leagues saves the leagues that are available for a sport

class SportLeague(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=125)
    league_id = models.IntegerField(blank=False, null=False, default=0)

    def __str__(self) -> str:
        return self.title

# Season stores the season id for the running leagues 
class Season(models.Model):
    season_id = models.IntegerField()
    league = models.ForeignKey(SportLeague, on_delete=models.RESTRICT)
    name = models.CharField(max_length=255)
    starting_date = models.DateField(default=now())
    ending_date = models.DateField(default=now())

    def __str__(self) -> str:
        return f"{self.name} {self.year}"

# Sport event comes from the games of different schedules 
class SportEvent(models.Model):
    event_id = models.IntegerField()
    league = models.ForeignKey(SportLeague, on_delete=models.RESTRICT)
    home_team = models.CharField(max_length=255)
    away_team = models.CharField(max_length=255)
    start_datetime = models.DateTimeField(default=now())
    status = models.CharField(max_length=50, choices=Sport_Status, default=Sport_Status['Not-Started'])
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.home_team} vs {self.away_team} / {self.league.title} / {self.start_datetime}"