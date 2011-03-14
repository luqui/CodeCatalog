from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail
from zoo.views import spec, editspec, snippet, search

urlpatterns = patterns('',
    (r'^spec/(?P<pk>\d+)/$', spec),
    (r'^spec/(?P<pk>\d+)/edit', editspec),
    (r'^(?P<pk>\d+)/$', snippet),
    (r'^search/$', search),
)
