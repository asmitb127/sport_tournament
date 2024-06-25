import datetime, json
from rest_framework import permissions, generics, views
from rest_framework.response import Response
from django.utils.timezone import now
from django.db.models import Q

from .seed_datas import get_leagues, get_seasons, get_schedule
from .models import Sport, SportLeague, Season, SportEvent
from .serializers.sport import SportEventSerializer, SportLeagueSerializer, SportListSerializer, SeasonListSerializer
from choices.choice  import Sport_Status

# Create your views here.
class SportView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def __init__(self):
        pass

    def get_current_leagues(self):
        try:
            leagues = get_leagues()
            # create sport for the first time
            sport = Sport.objects.create(
                title = 'Football'
            ).save()
            for league in leagues:
                current_league = SportLeague.objects.filter(league_id=league['idLeague'])
                #skip if already exists
                if current_league.exists():
                    continue
                #create new league
                else:
                    #create new league
                    newLeague = SportLeague.objects.create(
                        sport = sport,
                        title = league['strLeague'],
                        league_id = league['idLeague'],
                    ).save()
                    leagues.append(newLeague)

            #convert leagues to json format
            leagues_json = json.dumps(leagues)
            return Response(leagues_json)
        except Exception as e:
            print("exceptation on league", str(e))
            return Response(str(e))

    def get_participants(self, participants):
        home = ""
        away = ""
        for participant in participants:
            if participant['meta']['location'] == "home":
                home = participant['name']
            elif participant['meta']['location'] == "away":
                away = participant['name']
        return home, away

    def get_game_results(self, scores):
        home_score = 0
        away_score = 0
        for score in scores:
            if score["score"]["participant"] == "away":
                away_score += score["score"]["goals"]
            elif score["score"]["participant"] == "home":
                home_score += score["score"]["goals"]
        return home_score, away_score

    def get_running_events(self):
        try: 
            leagues = SportLeague.objects.all()
            for league in leagues:
                print("league", league)
                #events 
                events = get_schedule(league.league_id)
                print(f'events = {events} is for {league}')
                if events != None:
                    for event in events:
                        current_event = SportEvent.objects.filter(event_id=event['idEvent'])
                        event_time = datetime.datetime.strptime(event['strTimestamp'], '%Y-%m-%dT%H:%M:%S')
                        current_time = datetime.datetime.now()
                        #check if it is a past event
                        print(f'event = {event}')
                        if current_event and current_time > event_time:
                            #update the codebase for the event scores and check for the 
                            # reschedule of the events if any
                            #update the status of the current event 
                            current_event.home_score = event['intHomeScore']
                            current_event.away_score = event['intAwayScore']
                            current_event.status = event['strStatus']
                            if event['strPostponed'] == 'true':
                                current_event.start_datetime = event_time
                        else:
                            #create new event
                            current_event = SportEvent.objects.create(
                                event_id = event['idEvent'],
                                league = league,
                                home_team = event['strHomeTeam'],
                                away_team = event['strAwayTeam'],
                                start_datetime = event['strTimestamp'],
                                status = event['strStatus']
                            )
                        current_event.save()
        except Exception as e:
            print("exceptation on fetching leagues", str(e))
            return Response(str(e))



    def get(self, request):
        #get query 
        type = request.GET.get("type", None)
        print(f'type is {type}')

        try: 
            if type == 'leagues':
                self.get_current_leagues()
            else:
                self.get_running_events()
        except Exception as e:
            print("exceptation on get", str(e))
            return Response(str(e))
        
        return Response({ "success": "true" })


class SportEventList(generics.ListAPIView):
    queryset = SportEvent.objects.all()
    serializer_class = SportEventSerializer

    search_fields = ['league']
    order_fields = ['start_datetime', 'status']
    filterset_fields = ['league', 'event_id','status']

    def get_queryset(self):
        sport_event = SportEvent.objects.all()
        start_date = datetime.datetime.strptime(self.request.query_params.get('start_datetime'), '%Y-%m-%dT%H:%M:%S')
        end_date = datetime.datetime.strptime(self.request.query_params.get('end_datetime'), '%Y-%m-%dT%H:%M:%S')
        league_id = self.request.query_params.get('league_id')
        league =  SportLeague.objects.filter(pk=league_id)
        if league.exists():
            print("league", league)
            #filter the sport events with league 
            sport_event = sport_event.filter(league=league[0])
            print("sport event", sport_event)
            if start_date:
                sport_event = sport_event.filter(start_datetime__gte=start_date).filter(start_datetime__lte=end_date)
            self.queryset = sport_event
            return super().get_queryset()

class SportList(generics.ListAPIView):
    queryset = Sport.objects.all()
    serializer_class = SportListSerializer

class LeagueList(generics.ListAPIView):
    queryset = SportLeague.objects.all()
    serializer_class = SportLeagueSerializer

class SeasonList(generics.ListAPIView):
    queryset = Season.objects.select_related('league').all()
    serializer_class = SeasonListSerializer
