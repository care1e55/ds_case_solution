from datetime import datetime, timedelta
from typing import Iterable


SECONDS_IN_HOUR = 60 * 60
HOURS_IN_DAY = 24
WEEKENDS = (5, 6)
WORK_START_HOUR = 9
WORK_END_HOUR = 17


def to_datetime(date: str) -> datetime:
    return datetime.strptime(date, "%Y-%m-%d %H:%M:%S")


def is_workhour(date: datetime):
    if (date.weekday() in WEEKENDS) or (date.hour <= WORK_START_HOUR) or (date.hour > WORK_END_HOUR):
        return False
    return True


def hours(date_from: datetime, date_to: datetime) -> Iterable:
    delta = date_to - date_from
    for accumulated_hours in range(int(delta.total_seconds() // SECONDS_IN_HOUR) + 1):
        yield date_from + timedelta(hours=accumulated_hours)


def workhours(date_from: str, date_to: str) -> int:
    date_from, date_to = to_datetime(date_from), to_datetime(date_to)
    workhours_counter = 0
    for hour in hours(date_from, date_to):
        if is_workhour(hour):
            workhours_counter += 1
    return workhours_counter

if __name__ == '__main__':
    test_from_1 = "2019-12-02 08:00:00"
    test_to_1 = "2019-12-04 12:15:00"
    test_from_2 = "2019-12-01 09:30:00"
    test_to_2 = "2019-12-07 12:15:00"

    print(f'From {test_from_1} to {test_to_1} is {workhours(test_from_1, test_to_1)} workhours')
    print(f'From {test_from_2} to {test_to_2} is {workhours(test_from_2, test_to_2)} workhours')