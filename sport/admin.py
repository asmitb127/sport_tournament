from django.contrib import admin

# Register your models here.
from sport.models import Team, Sport, SportEvent, SportLeague, SportEventResult, Season, SeasonSportLeague

class TeamAdmin(admin.ModelAdmin):
    pass


admin.site.register(Team, TeamAdmin)
admin.site.register(Sport)
admin.site.register(SportEvent)
admin.site.register(SportLeague)
admin.site.register(SportEventResult)
admin.site.register(Season)
admin.site.register(SeasonSportLeague)