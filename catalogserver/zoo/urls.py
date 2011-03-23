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
    (r'^specs/(?P<versionptr>\d+)/active/$', jsonwrap(api.specs_active)),
    (r'^specs/(?P<versionptr>\d+)/all/$', jsonwrap(api.specs_all)),
    (r'^specs/(?P<versionptr>\d+)/snippets/$', jsonwrap(api.specs_snippets)),
    (r'^specs/(?P<versionptr>\d+)/snippets/active/$', jsonwrap(api.specs_snippets_active)),
    (r'^spec/(?P<version>\d+)/$', jsonwrap(api.spec)),
    (r'^snippets/(?P<versionptr>\d+)/active/$', jsonwrap(api.snippets_active)),
    (r'^snippets/(?P<versionptr>\d+)/all/$', jsonwrap(api.snippets_all)),
    (r'^snippet/(?P<version>\d+)/$', jsonwrap(api.snippet)),
    (r'^new/snippet/$', jsonwrap(api.new_snippet)),
    (r'^new/spec/$', jsonwrap(api.new_spec)),
    (r'^vote/$', jsonwrap(api.vote)),
)
    

urlpatterns = patterns('',
    (r'^api/', include(apipatterns)),
    (r'^spec/(?P<pk>\d+)/$', views.spec),
    (r'^search/$', include('haystack.urls')),
    (r'^new/$', views.new),
    (r'^static/(?P<path>[\w+\./-]+)$', views.static),
    (r'^openid/', include('django_openid_auth.urls')),
    (r'^logout/$', 'django.contrib.auth.views.logout'),
)
