from django_seed import Seed
import requests, logging

import environ, os
from pathlib import Path

from sport.models import Sport, Season, SportLeague, SeasonSportLeague, Team, SportEvent

logger = logging.getLogger(__name__)
logging.basicConfig(filename='log.log', encoding='utf-8', level=logging.DEBUG)
# logging.basicConfig(level=logging.DEBUG)

env = environ.Env(DEBUG=(bool, False))
BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

seeder = Seed.seeder()

# add path of api
path={
    'competition': '/en/competitions',
    'competition_season': '/en/competitions/:urn_competition/seasons',
}

def get_full_path(path, query=''):
    '''
    Get full path per api.
    '''
    url = env('baseUrl')
    format = env('format')
    api_key = env('api_key')
    return f"{url}{path}.{format}?api_key={api_key}{query}"


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
                current_season = Season.objects.filter(season_id=each['id'])
                if not current_season.exists():
                    current_season = Season.objects.create(
                        season_id=each['id'],
                        name=each['name'],
                        year=each['year']
                    )
                else:
                    current_season=current_season.get()
                if not SeasonSportLeague.objects.filter(season=current_season).filter(league=each_comp).filter(start_date= each['start_date']).filter(end_date= each['end_date']).exists():
                    SeasonSportLeague.objects.create(
                        season = current_season,
                        league = each_comp,
                        start_date = each['start_date'],
                        end_date = each['end_date'],
                    )

def run_seeder():
    # get_compettion()
    get_season_competition()
    # seeder = Seed.seeder()
    # seeder.add_entity(MyModel, 10)
    # seeder.execute()


