from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail
from zoo import views
from zoo import api

# CodeCatalog Snippet http://codecatalog.net/25/
def jsonwrap(f):
    from django.http import HttpResponse
    import json
    
    def cb(*args, **kwargs):
        return HttpResponse(content=json.dumps(f(*args, **kwargs)), mimetype='application/json')
    return cb
# End CodeCatalog Snippet

apipatterns = patterns('',
    (r'^snippet/(?P<pk>\d+)/get/$', jsonwrap(api.get_snippet)),
    (r'^snippet/put/$', jsonwrap(api.put_snippet))
)
    

urlpatterns = patterns('',
    (r'^api/', include(apipatterns)),
    (r'^spec/(?P<pk>\d+)/$', views.spec),
    (r'^spec/(?P<pk>\d+)/edit/$', views.edit_spec),
    (r'^(?P<pk>\d+)/$', views.snippet),
    (r'^(?P<pk>\d+)/raw/$', views.raw_snippet),
    (r'^(?P<pk>\d+)/branch/$', views.branch_snippet),
    (r'^(?P<pk>\d+)/delete/$', views.delete_snippet),
    (r'^(?P<pk>\d+)/setcanon/$', views.set_canon),
    (r'^(?P<pk>\d+)/vote/(?P<val>-1|0|1)/$', views.vote_snippet),
    (r'^search/$', include('haystack.urls')),
    (r'^new/$', views.new),
    (r'^static/(?P<path>[\w+\./-]+)$', views.static),
    (r'^openid/', include('django_openid_auth.urls')),
    (r'^logout/$', 'django.contrib.auth.views.logout'),
)
