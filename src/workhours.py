from enum import Enum
from datetime import datetime, timedelta
from typing import Iterable


# class Weekend(Enum):
#     SATURDAY = 5
#     SUNDAY = 6
#

SECONDS_IN_HOUR = 60 * 60
HOURS_IN_DAY = 24
WEEKENDS = (5, 6)
WORK_START = datetime(hour=9)
WORK_END = datetime(hour=17)


def to_datetime(date: str) -> datetime:
    return datetime.strptime(date, "%Y-%m-%d %H:%M:%S")


def dates(date_from: datetime, date_to: datetime) -> Iterable:
    delta = date_to - date_from
    for days in range(delta.days + 1):
        yield date_from + timedelta(days)


def weekends(date_from: datetime, date_to: datetime) -> int:
    weekend_counter = 0
    for date in dates(date_from, date_to):
        if date.weekday() in WEEKENDS:
            weekend_counter += 1
    return weekend_counter


def workhours(date_from: str, date_to: str) -> int:
    date_from, date_to = to_datetime(date_from), to_datetime(date_to)
    return int((date_to - date_from).total_seconds() // SECONDS_IN_HOUR) - weekends(date_to, date_from) * HOURS_IN_DAY
