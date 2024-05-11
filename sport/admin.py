from django.contrib import admin

# Register your models here.
from sport.models import  Sport, SportEvent, SportLeague, Season

# class TeamAdmin(admin.ModelAdmin):
#     pass


admin.site.register(Sport)
admin.site.register(SportEvent)
admin.site.register(SportLeague)
admin.site.register(Season)