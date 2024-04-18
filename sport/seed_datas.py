from django_seed import Seed
import requests, logging

from sport.models import Sport, Season, SportLeague, SeasonSportLeague, Team, SportEvent
from sport.api import path, get_full_path

logger = logging.getLogger(__name__)
# logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)

seeder = Seed.seeder()


# headers = {'User-Agent': 'My User Agent'}
def get_compettion():
    url_path = get_full_path(path['competition'])
    response = requests.get(url_path)
    logging.info('response %s', response)
    data = response.json()
    sport = Sport.objects.first()
    for each in data.get("competitions"):
        #skip if already exists
        current_league = SportLeague.objects.filter(competition_id=each['id'])
        if current_league.exists():
            continue
        else:
            #create new league
            SportLeague.objects.create(
                sport = sport,
                title = each['name'],
                competition_id = each['id'],
            ).save()

def get_season_competition():

    '''
    Season competition with query.
    '''
    competition = SportLeague.objects.all().iterator()
    for each_comp in competition:
        query = f'''&start_date=2023-01-01&end_date=2024-12-30'''
        url_path = get_full_path(f'/en/competitions/{each_comp.competition_id}/seasons', query)
        response = requests.get(url_path)
        logging.info('response %s', response)
        data = response.json()
        if response.status_code == 200:
            for each in data.get('seasons'):
                # if not SeasonSportLeague.objects.filter(competition_id=each.get('id')).exists():
                current_season = Season.objects.filter(season_id=each['id'])
                if current_season.exists():
                    if not SeasonSportLeague.objects.filter(season=current_season).exists():
                        SeasonSportLeague.objects.create(
                            competition = each_comp,
                            season_id = each['id'],
                            start_datetime = each['start_date'],
                            end_datetime = each['end_date'],
                        )

def run_seeder():
    # get_compettion()
    get_season_competition()
    # seeder = Seed.seeder()
    # seeder.add_entity(MyModel, 10)
    # seeder.execute()


