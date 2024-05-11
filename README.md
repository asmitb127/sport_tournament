## Model info with Soccer API SportTrader.
#### Sports:
        1. Team -> Competitors
        2. Sport
        3. SportLeague -> Competitions
        5. Season SportLeague -> Competiton Season
        5. SportEvent
        6. SportEventResult

### Use API

    1. Competitions
    2. Competition Season
    3. Season Lineups

### Debug log
        tail -f log.log


### Run seed
    1. python manage.py shell
    2. from sport.seed_datas import run_seeder
    3. run_seeder()
