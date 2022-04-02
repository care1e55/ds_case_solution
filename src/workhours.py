from enum import Enum
from datetime import datetime, timedelta
from typing import Iterable


class Weekend(Enum):
    SATURDAY = 5
    SUNDAY = 6


SECONDS_IN_HOUR = 60 * 60
WEEKENDS = (Weekend.SATURDAY, Weekend.SUNDAY)


def to_datetime(date: str) -> datetime:
    return datetime.strptime(date, "%Y-%m-%d %H:%M:%S")


def dates(date_from: datetime, date_to: datetime) -> Iterable:
    delta = date_to - date_from
    for days in range(delta.days):
        yield date_from + timedelta((date_to - date_from).days)


def count_weekends(date_from: datetime, date_to: datetime) -> int:
    weekend_counter = 0
    for date in dates(date_from, date_to):
        if date.weekday() in WEEKENDS:
            weekend_counter += 1
    return weekend_counter


def count_workhours(date_from: str, date_to: str) -> int:
    date_from, date_to = to_datetime(date_from), to_datetime(date_to)
    weekends_count = count_weekends(date_to - date_from)
    workhours = (date_to - date_from).total_seconds() // SECONDS_IN_HOUR - weekends_count
    return int(workhours)
