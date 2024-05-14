from django.urls import path, include
from rest_framework import routers

from .views import add_pool_entry, TournamentViewSet, PoolEntryViewSet

router = routers.DefaultRouter()
router.register(r'create', TournamentViewSet, basename="tournament-create")
router.register(r'list', PoolEntryViewSet, basename="list")
urlpatterns = [
    path('', include(router.urls)),
    path('add-pool-entry/', add_pool_entry, name='addentry')
]