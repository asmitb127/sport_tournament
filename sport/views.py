import datetime, json
from rest_framework import permissions, generics, views
from rest_framework.response import Response
from .seed_datas import get_leagues, get_seasons, get_schedule
from .models import Sport, SportLeague, Season, SportEvent


# Create your views here.
class SportView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def __init__(self):
        pass

    def get_current_leagues(request):
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
            return Response(str(e))

    def get_running_seasons(request):
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
                                start_date = season['start_date'],
                                end_date = season['end_date'],
                            ).save()

            seasons_json = json.dumps(seasons)
            return Response(seasons_json)
        except Exception as e:
            return Response(str(e))

    def get_participants(participants):
        home = ""
        away = ""
        for participant in participants:
            if participant['meta']['location'] == "home":
                home = participant['name']
            elif participant['meta']['location'] == "away":
                away = participant['name']
        return home, away

    def get_game_results(scores):
        home_score = 0
        away_score = 0
        for score in scores:
            if score["score"]["participant"] == "away":
                away_score += score["score"]["goals"]
            elif score["score"]["participant"] == "home":
                home_score += score["score"]["goals"]
        return home_score, away_score

    def get_running_schedule(self, request):
        try: 
            seasons = Season.objects.filter(end_date__gte=datetime.now())
            for season in seasons:
                schedule = get_schedule(season.season_id)
                for rounds in schedule:
                    for event in rounds:
                        current_event = SportEvent.objects.filter(event_id=event['id'])
                        if current_event.exists():
                            home_score, away_score = self.get_game_results(event['scores'])
                            current_event.update(
                                home_score = home_score,
                                away_score = away_score,
                                status = "updated",
                            )
                        else:
                            home_team, away_team = self.get_participants(event['participants'])
                            SportEvent.objects.create(
                                event_id = event['id'],
                                league = season.league,
                                home_team = home_team,
                                away_team = away_team,
                                start_datetime = event['start_datetime'],
                                status = "running",
                            ).save()


        except Exception as e:
            return Response(str(e))

    def get(self, request):
        type = request.get('type', None)

        if type == 'leagues':
            return self.get_current_leagues(request)
        elif type == 'seasons':
            return self.get_running_seasons(request)
        elif type == 'schedule':
            return self.get_running_schedule(request)


def get_seasons(request):
    pass

    
        



