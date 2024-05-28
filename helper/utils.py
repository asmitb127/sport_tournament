from datetime import datetime


def get_week_from_date(start_date, end_date):
    today_date = datetime.now().date()
    difference = (today_date - start_date).days
    current_week_number = (difference // 7) + 1
    return current_week_number