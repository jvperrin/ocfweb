from django.conf.urls import url

from ocfweb.stats.accounts import stats_accounts
from ocfweb.stats.daily_graph import daily_graph_image
from ocfweb.stats.job_frequency import daily_jobs_image
from ocfweb.stats.mirrors import stats_mirrors
from ocfweb.stats.printing import pages_printed
from ocfweb.stats.printing import semester_histogram
from ocfweb.stats.printing import stats_printing
from ocfweb.stats.semester_job import weekday_jobs_image
from ocfweb.stats.semester_job import weekend_jobs_image
from ocfweb.stats.session_count import session_count_image
from ocfweb.stats.session_length import session_length_image
from ocfweb.stats.session_stats import session_stats
from ocfweb.stats.summary import summary

urlpatterns = [
    url(r'^$', summary, name='stats'),
    url(r'^daily-graph/graph$', daily_graph_image, name='daily_graph_image'),
    url(r'^session-count/graph$', session_count_image, name='session_count_image'),
    url(r'^session-length/graph$', session_length_image, name='session_length_image'),
    url(r'^printing/$', stats_printing, name='stats_printing'),
    url(r'^accounts/$', stats_accounts, name='stats_accounts'),
    url(r'^printing/semester-histogram/graph$', semester_histogram, name='semester_histogram'),
    url(r'^printing/pages-printed$', pages_printed, name='pages_printed'),
    url(r'^printing/daily-job/graph$', daily_jobs_image, name='daily_job_image'),
    url(r'^printing/weekend-jobs/graph$', weekend_jobs_image, name='weekend_jobs_image'),
    url(r'^printing/weekday-jobs/graph$', weekday_jobs_image, name='weekday_jobs_image'),

    url(r'^mirrors/$', stats_mirrors, name='stats_mirrors'),
    url(r'^session-stats/$', session_stats, name='session-stats'),
]
