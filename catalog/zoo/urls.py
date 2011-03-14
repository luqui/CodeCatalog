from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail
from zoo.views import spec, edit_spec, snippet, edit_snippet, search, new

urlpatterns = patterns('',
    (r'^spec/(?P<pk>\d+)/$', spec),
    (r'^spec/(?P<pk>\d+)/edit/$', edit_spec),
    (r'^(?P<pk>\d+)/$', snippet),
    (r'^(?P<pk>\d+)/edit/$', edit_snippet),
    (r'^search/$', search),
    (r'^new/$', new),
)
