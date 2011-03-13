from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail
from zoo.views import spec, snippet

urlpatterns = patterns('',
    (r'^spec/(?P<pk>\d+)/$', spec),
    (r'^snippet/(?P<pk>\d+)/$', snippet),
)
