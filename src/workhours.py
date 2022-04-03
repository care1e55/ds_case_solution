from datetime import datetime, timedelta
from typing import Iterable

import typer as typer

SECONDS_IN_HOUR = 60 * 60
WEEKENDS = (5, 6)
WORK_START_HOUR = 9
WORK_END_HOUR = 17


app = typer.Typer()


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


@app.command()
def workhours(
    date_from: str = typer.Option(...),
    date_to: str = typer.Option(...)
) -> int:
    datetime_from, datetime_to = to_datetime(date_from), to_datetime(date_to)
    workhours_counter = 0
    for hour in hours(datetime_from, datetime_to):
        if is_workhour(hour):
            workhours_counter += 1
    typer.echo(f'From {date_from} to {date_to} is {workhours_counter} workhours')
    return workhours_counter


if __name__ == '__main__':
    app()
