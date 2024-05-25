from django.urls import path, include
from rest_framework import routers

from .views import TournamentViewSet, PoolEntryViewSet, AddPoolEntry, MyTournamentViewSet

router = routers.DefaultRouter()
router.register(r'create', TournamentViewSet, basename="tournament-create")
router.register(r'list', PoolEntryViewSet, basename="list")

urlpatterns = [
    path('', include(router.urls)),
    path('add-pool-entry/', AddPoolEntry.as_view(), name='addentry'),
    path('my-pool/', MyTournamentViewSet.as_view(), name='my_pool'),
]