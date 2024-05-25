from rest_framework import viewsets, views, status, generics
from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions

from core.custom_permissions import TokenAuthentications
from sport.models import Sport, SportEvent
from tournament.models import Tournament, PoolEntry, Picks

from tournament.serializers.tournament import TournamentSerializer, TournamentListSerializer
from tournament.serializers.pool_entry import PoolEntrySerializer,PoolEntryEventSerializer


class TournamentViewSet(viewsets.ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    authentication_classes = [TokenAuthentications]
    permission_classes = [permissions.IsAuthenticated,]

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ['retrieve', 'list']:
            return TournamentListSerializer
        return TournamentSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.__dict__.update({'player_count': instance.pool_entry.count()})
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        for each in queryset:
            each.__dict__.update({'player_count': each.pool_entry.count()})
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class AddPoolEntry(views.APIView):
    authentication_classes = [TokenAuthentications]
    permission_classes = [permissions.IsAuthenticated,]

    def post(self, request):
        tournament_id = request.data['tournament_id']
        if not Tournament.objects.filter(id=tournament_id).exists():
            return Response({'error': 'Tournament does not exist'}, status=400)

        if PoolEntry.objects.filter(tournament__id=tournament_id).exists():
            return Response({'error': 'You have already picked for this tournament.'}, status=400)

        pool_entry = PoolEntry.objects.create(
            tournament=Tournament.objects.get(id=tournament_id),
            entry_txn=request.data.get('entry_txn') or 1,
            network=request.data.get('network') or 1,
            player_id=request.user.id
        )
        pool_entry.save()

        for pick in request.data['picks']:
            sport_event = SportEvent.objects.get(event_id=pick['event_id'])
            Picks.objects.create(
                pool_entry=pool_entry,
                event_id=sport_event,
                pick=pick['pick']
            ).save()

        return Response({'success': 'Pool entry added'}, status=status.HTTP_200_OK)

class PoolEntryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PoolEntry.objects.all()
    serializer_class = PoolEntrySerializer

    # def get_queryset(self):
    #     queryset = PoolEntry.objects.all()
    #     return queryset

class MyTournamentViewSet(generics.ListAPIView):
    authentication_classes = [TokenAuthentications]
    permission_classes = [permissions.IsAuthenticated,]
    queryset = Tournament.objects.all()
    serializer_class = PoolEntryEventSerializer

    def get_queryset(self):
        return Tournament.objects.all()

    def get(self, request):
        queryset = self.get_queryset().filter(my_pool_entry__player=request.user)
        data = self.get_serializer(queryset, many=True, context=request).data
        return Response({'sucess': 'User Pool entry fetched.', 'data': data}, status=status.HTTP_200_OK)