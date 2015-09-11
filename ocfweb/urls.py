import re

from django.conf.urls import url

from ocfweb.docs.docs import doc
from ocfweb.docs.docs import docs_index
from ocfweb.docs.docs import list_doc_names
from ocfweb.main.favicon import favicon
from ocfweb.main.home import home
from ocfweb.main.staff_hours import staff_hours
from ocfweb.main.servers import servers


def doc_name(doc_name):
    # we can't actually deal with escaping into a regex, so we just use a whitelist
    assert re.match('^/[a-zA-Z\-/]+$', doc_name)
    return doc_name[1:].replace('-', '\-')

doc_names = '|'.join(map(doc_name, list_doc_names()))

urlpatterns = [
    url('^$', home, name='home'),
    url('^favicon.ico$', favicon, name='favicon'),
    url('^staff-hours$', staff_hours, name='staff-hours'),
    url('^servers$', servers, name='servers'),

    url('^docs/$', docs_index, name='docs'),
    # we use a complicated generated regex here so that we have actual
    # validation of URLs (in other words, if you try to make a link to a
    # missing document, it will fail)
    url('^docs/({doc_names})/$'.format(doc_names=doc_names), doc, name='doc'),
]
