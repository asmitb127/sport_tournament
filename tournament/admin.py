from django.contrib import admin

# Register your models here.
from tournament.models import Tournament, TournamentPool

admin.site.register(Tournament)
admin.site.register(TournamentPool)