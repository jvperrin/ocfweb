from datetime import datetime

from ocflib.lab.hours import Day
from ocflib.lab.hours import REGULAR_HOURS


def get_open_close(day):
    """Return datetime objects representing open and close for a day rounded
    down to the hour.

    If the lab is closed all day (e.g. holiday), just return our weekday hours.
    """
    d = Day.from_date(day)

    if not d.closed_all_day:
        start = datetime(day.year, day.month, day.day, min(h.open.hour for h in d.hours))
        end = datetime(day.year, day.month, day.day, max(h.close.hour for h in d.hours))
    else:
        start = datetime(day.year, day.month, day.day, min(h.open for h in
                                                           REGULAR_HOURS[None].hour))
        end = datetime(day.year, day.month, day.day, max(h.close for h in REGULAR_HOURS[None].hour))

    return start, end
