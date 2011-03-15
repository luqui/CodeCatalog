from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail
from zoo.views import spec, edit_spec, snippet, raw_snippet, edit_snippet, new

urlpatterns = patterns('',
    (r'^spec/(?P<pk>\d+)/$', spec),
    (r'^spec/(?P<pk>\d+)/edit/$', edit_spec),
    (r'^(?P<pk>\d+)/$', snippet),
    (r'^(?P<pk>\d+)/raw/$', raw_snippet),
    (r'^(?P<pk>\d+)/edit/$', edit_snippet),
    (r'^search/$', include('haystack.urls')),
    (r'^new/$', new),
)
