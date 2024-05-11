import datetime, json
from rest_framework import permissions, generics, views
from rest_framework.response import Response
from .seed_datas import get_leagues, get_seasons, get_schedule
from .models import Sport, SportLeague, Season, SportEvent
from django.utils.timezone import now
from .serializers import SportEventSerializer, SportListSerializer, SeasonListSerializer
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
                current_league = SportLeague.objects.filter(league_id=league['id'])
                #skip if already exists
                if current_league.exists():
                    continue
                #create new league
                else:
                    if league['active']:
                        #create new league
                        newLeague = SportLeague.objects.create(
                            sport = sport,
                            title = league['name'],
                            league_id = league['id'],
                        ).save()
                        leagues.append(newLeague)

            #convert leagues to json format
            leagues_json = json.dumps(leagues)
            return Response(leagues_json)
        except Exception as e:
            print("exceptation on league", str(e))
            return Response(str(e))

    def get_running_seasons(self):
        try:
            seasons = get_seasons()
            for season in seasons:
                current_season = Season.objects.filter(season_id=season['id'])
                #skip if already exists
                if current_season.exists():
                    continue
                #create new season
                else:
                    if not season['finished']:
                        #create new season
                        league = SportLeague.objects.get(league_id=season['league_id'])
                        if league:
                            Season.objects.create(
                                season_id = season['id'],
                                league = league,
                                name = season['name'],
                                starting_date = season['starting_at'],
                                ending_date = season['ending_at'],
                            ).save()

            seasons_json = json.dumps(seasons)
            return Response(seasons_json)
        except Exception as e:
            print("exceptation on season", str(e))
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

    def get_running_schedule(self):
        try: 
            seasons = Season.objects.filter(ending_date__gte=now())
            if seasons.exists():
                for season in seasons:
                    schedule = get_schedule(season.season_id)
                    for rounds in schedule:
                        for round in rounds['rounds']:
                            for fixture in round['fixtures']:
                                current_event = SportEvent.objects.filter(event_id=fixture['id'])
                                
                                if current_event.exists():
                                    if len(fixture['scores']) > 0:
                                        home_score, away_score = self.get_game_results(fixture['scores'])
                                        
                                        if home_score >0 | away_score > 0:
                                            current_event.update(
                                                home_score = home_score,
                                                away_score = away_score,
                                            )
                                        
                                        if len(str(fixture['details']))>5:
                                            current_event.update(
                                                status = Sport_Status['Ended']
                                            )
                                        else:
                                            current_event.update(
                                                status = Sport_Status['Active']
                                            )
                                    else:
                                        current_event.update(
                                            status = Sport_Status['Not-Started']
                                        ) 

                                else:
                                    if fixture['starting_at_timestamp'] > now().timestamp():
                                        
                                        home_team, away_team = self.get_participants(fixture['participants'])
                                        SportEvent.objects.create(
                                            event_id = fixture['id'],
                                            season = season,
                                            league = season.league,
                                            home_team = home_team,
                                            away_team = away_team,
                                            start_datetime = fixture['starting_at'],
                                            status = Sport_Status['Not-Started']
                                        ).save()
                                

        except Exception as e:
            print("exceptation on schedule", str(e))
            return Response(str(e))

    def get(self, request):
        #get query 
        type = request.GET.get("type", None)
        print(f'type is {type}')

        try: 
            if type == 'seasons':
                self.get_current_leagues()
                self.get_running_seasons()
            else:
                self.get_running_schedule()
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

class SportList(generics.ListAPIView):
    queryset = Sport.objects.all()
    serializer_class = SportListSerializer

class SeasonList(generics.ListAPIView):
    queryset = Season.objects.select_related('league').all()
    serializer_class = SeasonListSerializer
