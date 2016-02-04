import logging
from datetime import date
from datetime import datetime
from datetime import timedelta
from operator import attrgetter

from django.shortcuts import render
from ocflib.constants import CURRENT_SEMESTER_START
from ocflib.lab.printing import get_maintkit
from ocflib.lab.printing import get_toner
from ocflib.lab.printing import PRINTERS
from ocflib.lab.stats import list_desktops
from ocflib.lab.stats import staff_in_lab as real_staff_in_lab
from ocflib.lab.stats import STATS_EPOCH
from ocflib.lab.stats import top_staff_alltime as real_top_staff_alltime
from ocflib.lab.stats import top_staff_semester as real_top_staff_semester
from ocflib.lab.stats import users_in_lab_count as real_users_in_lab_count
from ocflib.lab.stats import UtilizationProfile

from ocfweb.caching import periodic
from ocfweb.stats.daily_graph import get_open_close

def datetime_to_js(dt):
    """Convert a Python datetime object into a format recognized
    by JavaScript to display using Highcharts

    Date.UTC(year, month[, day[, hour[, minute[, second[, millisecond]]]]])

    month: An integer between 0-11 (I have no idea why this is zero indexed, but whatever)
    """
    return "Date.UTC({}, {}, {}, {}, {})".format(dt.year, dt.month - 1, dt.day, dt.hour, dt.minute)

_logger = logging.getLogger(__name__)


def get_stats_start_end(date_):
    """Get the start and end times for a day on the stats graph"""
    start, end = get_open_close(date_)
    now = datetime.today()

    # If the lab has opened, but hasn't closed yet, only count
    # statistics until the current time. If the lab isn't open
    # yet, then don't count anything, and if it is closed, show
    # statistics from when it was open during the day.
    if now > start and now < end:
        end = now
    elif now <= start:
        end = start

    return start, end


@periodic(60)
def desktop_profiles():
    start, end = get_stats_start_end(date.today())

    return sorted(
        UtilizationProfile.from_hostnames(list_desktops(), start, end).values(),
        key=attrgetter('hostname'),
    )


@periodic(60)
def graph_data():
    start, end = get_stats_start_end(date.today())

    profiles = UtilizationProfile.from_hostnames(list_desktops(public_only=True), start, end).values()
    minutes = int((end - start).total_seconds() // 60)

    usage = []
    for minute in range(minutes):
        instant15 = start + timedelta(minutes=minute, seconds=15)
        instant45 = start + timedelta(minutes=minute, seconds=45)
        in_use = sum(1 if profile.in_use(instant15)
                     or profile.in_use(instant45) else 0 for profile in profiles)
        usage.append([datetime_to_js(start + timedelta(minutes=minute)), in_use])

    # Remove single quotes, since the array has strings representing
    # JS Date.UTC objects and we want Date.UTC objects without quotes
    return str(usage).replace('\'', '')


@periodic(30)
def staff_in_lab():
    return real_staff_in_lab()


@periodic(300)
def top_staff_alltime():
    return real_top_staff_alltime()


@periodic(300)
def top_staff_semester():
    return real_top_staff_semester()


@periodic(30)
def users_in_lab_count():
    return real_users_in_lab_count()


@periodic(60)
def printers():
    def silence(f):
        def inner(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except OSError as ex:
                _logger.warn('Silencing exception reading printer data: {}'.format(ex))
                return None
        return inner

    return sorted(
        (printer, silence(get_toner)(printer), silence(get_maintkit)(printer))
        for printer in PRINTERS
    )


def summary(request):
    start, end = get_open_close(date.today())

    return render(
        request,
        'summary.html',
        {
            'title': 'Lab Statistics',
            'desktop_profiles': desktop_profiles(),
            'current_semester_start': CURRENT_SEMESTER_START,
            'stats_epoch': STATS_EPOCH,
            'staff_in_lab': staff_in_lab(),
            'top_staff_alltime': top_staff_alltime()[:10],
            'top_staff_semester': top_staff_semester()[:10],
            'users_in_lab_count': users_in_lab_count(),
            'printers': printers(),
            'graph_data': graph_data(),
            'date': date.today().strftime('%a %b %d, %Y'),
            'chart_start': datetime_to_js(start),
            'chart_end': datetime_to_js(end),
        },
    )

