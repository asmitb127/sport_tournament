from rest_framework import viewsets

from tournament.serializers import TournamentSerializer, PoolEntrySerializer
from tournament.models import Tournament, PoolEntry


class TournamentViewSet(viewsets.ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

    def perform_create(self, serializer):
        self.created_by = self.request.user
        return super().perform_create(serializer)
    
    # def get_queryset(self):
    #     #create a queryset to get the tournament and events
        
    #     queryset = Tournament.objects.all()
        
    #     return queryset


class PoolEntryViewSet(viewsets.GenericViewSet, viewsets.mixins.CreateModelMixin, viewsets.mixins.ListModelMixin, viewsets.mixins.RetrieveModelMixin, viewsets.mixins.UpdateModelMixin, viewsets.mixins.DestroyModelMixin):
    queryset = PoolEntry.objects.all()
    serializer_class = PoolEntrySerializer


    def perform_create(self, serializer):
        self.created_by = self.request.user
        return super().perform_create(serializer)

    def get_queryset(self):
        queryset = PoolEntry.objects.all()
        
        return queryset
