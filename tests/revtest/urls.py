from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^T1/$', 'revtest.views.test_view', name="URL1"),
    url(r'^T2/([0-9]+)/$', 'revtest.views.test_view', name="URL2"),
    url(r'^T3/(?P<x>[0-9]+)/(?P<y>[0-9]+)/(?P<z>[0-9]+)/$', 'revtest.views.test_view', name="URL3"),
)
