from datetime import datetime
from datetime import timedelta

from ocflib.lab.hours import Day

def get_open_close(day):
    """Return datetime objects representing open and close for a day.

    If the lab is closed all day (e.g. holiday), just return our weekday hours.
    """
    d = Day.from_date(day)

    if not d.closed_all_day:
        start = datetime(day.year, day.month, day.day, min(h.open for h in d.hours))
        end = datetime(day.year, day.month, day.day, max(h.close for h in d.hours))
    else:
        start = datetime(day.year, day.month, day.day, min(h.open for h in REGULAR_HOURS[None]))
        end = datetime(day.year, day.month, day.day, max(h.close for h in REGULAR_HOURS[None]))

    return start, end

