from django.urls import path, include
from rest_framework import routers

from tournament import views

router = routers.DefaultRouter()
router.register(r'create', views.TournamentViewSet, basename="tournament-create")
router.register(r'list', views.PoolEntryViewSet, basename="list")

urlpatterns = [
    path('', include(router.urls)),
    path('add-pool-entry/', views.AddPoolEntry.as_view(), name='addentry'),
    path('my/',
         include([
             path('pool/',
                  include([
                      path('', views. MyPoolPickUpViewSet.as_view(), name='my_pool'),
                      path('leaderboard/', views. MyPoolLeaderViewSet.as_view(), name='my_pool_leaderboard'),
                  ])
             )
         ])
        )
]