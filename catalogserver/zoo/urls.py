from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail
from zoo import views

urlpatterns = patterns('',
    (r'^spec/(?P<pk>\d+)/$', views.spec),
    (r'^spec/(?P<pk>\d+)/edit/$', views.edit_spec),
    (r'^spec/(?P<pk>\d+)/new/$', views.new_for_spec),
    (r'^(?P<pk>\d+)/$', views.snippet),
    (r'^(?P<pk>\d+)/raw/$', views.raw_snippet),
    (r'^(?P<pk>\d+)/branch/$', views.branch_snippet),
    (r'^(?P<pk>\d+)/delete/$', views.delete_snippet),
    (r'^(?P<pk>\d+)/setcanon/$', views.set_canon),
    (r'^search/$', include('haystack.urls')),
    (r'^new/$', views.new),
    (r'^static/(?P<path>[\w+\./-]+)$', views.static),
    (r'^openid/', include('django_openid_auth.urls')),
)
