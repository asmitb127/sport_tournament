from django.urls import path, include
from rest_framework import routers

from tournament import views


router = routers.DefaultRouter()
router.register(r'view', views.TournamentViewSet, basename="tournament")

urlpatterns = [
    path('', include(router.urls)),
]