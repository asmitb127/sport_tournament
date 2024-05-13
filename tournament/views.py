from rest_framework import viewsets
from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response as JSONResponse
from rest_framework import permissions

from core.custom_permissions import TokenAuthentications
from sport.models import Sport, SportEvent
from tournament.serializers import TournamentSerializer, PoolEntrySerializer
from tournament.models import Tournament, PoolEntry, Picks


class TournamentViewSet(viewsets.ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    authentication_classes = [TokenAuthentications]


def validate_join_time(value):
    if value < datetime.now():
        return False
    return value

def validate_picks(value):
    for pick in value:
        if not SportEvent.objects.filter(event_id=pick['event_id']).exists():
            return False
    return value



@api_view(['POST'])
def add_pool_entry(request):
    # add a pool entry for the tournament

    if request.method == 'POST':
        tournament_id = request.data['tournament_id']
        if not Tournament.objects.filter(tournament_id=tournament_id).exists():
            return JSONResponse({'error': 'Tournament does not exist'}, status=400)

        pool_entry = PoolEntry.objects.create(
            tournament=Tournament.objects.get(tournament_id=tournament_id),
            entry_txn=request.data['entry_txn'],
            network=request.data['network'],
            join_time=request.data['join_time']
        )
        pool_entry.save()

        for pick in request.data['picks']:
            sport_event = SportEvent.objects.get(event_id=pick['event_id'])
            Picks.objects.create(
                pool_entry=pool_entry,
                event_id=sport_event,
                pick=pick['pick']
            ).save()

        return JSONResponse({'success': 'Pool entry added'}, status=200)
    

class PoolEntryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PoolEntry.objects.all()
    serializer_class = PoolEntrySerializer

    def get_queryset(self):
        queryset = PoolEntry.objects.all()
        
        return queryset
