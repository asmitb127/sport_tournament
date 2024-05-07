from rest_framework import viewsets

from tournament.serializers import TournamentSerializer
from tournament.models import Tournament, TournamentPool


class TournamentViewSet(viewsets.ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)