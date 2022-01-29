from datetime import datetime


def date(str):
    return datetime.strptime(str, '%Y-%m-%d').date()
