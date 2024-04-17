import environ, os
from pathlib import Path

env = environ.Env(DEBUG=(bool, False))
BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

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

