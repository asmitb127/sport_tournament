from django.contrib import admin
from django.urls import path, include 

from sport.views import SportView, SportEventList, SportList, SeasonList

urlpatterns = [
    path('fetch/', SportView.as_view(), name='fetch'),
    path('sport-events/', SportEventList.as_view(), name='SportEventList'),
    path('sport-list/', SportList.as_view(), name='SportList'),
    path('season-list/', SeasonList.as_view(), name='SeasonList'),
]