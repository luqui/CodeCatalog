from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail
import django.views.static
from zoo import views
from zoo import api

def jsonwrap(f):
    from django.http import HttpResponse
    import json
    
    def cb(*args, **kwargs):
        datastructure = f(*args, **kwargs)
        return HttpResponse(content=json.dumps(datastructure), mimetype='application/json')
    return cb

apipatterns = patterns('',
    (r'^specs/(?P<versionptr>\d+)/active/$', jsonwrap(api.specs_active)),
    (r'^specs/(?P<versionptr>\d+)/all/$', jsonwrap(api.specs_all)),
    (r'^specs/(?P<versionptr>\d+)/snippets/$', jsonwrap(api.specs_snippets)),
    (r'^specs/(?P<versionptr>\d+)/snippets/active/$', jsonwrap(api.specs_snippets_active)),
    (r'^specs/(?P<versionptr>\d+)/assemble/$', jsonwrap(api.assemble)),
    (r'^specs/(?P<versionptr>\d+)/bugs/active/$', jsonwrap(api.bugs)),
    (r'^spec/(?P<version>\d+)/$', jsonwrap(api.spec)),
    (r'^snippets/(?P<versionptr>\d+)/active/$', jsonwrap(api.snippets_active)),
    (r'^snippets/(?P<versionptr>\d+)/all/$', jsonwrap(api.snippets_all)),
    (r'^snippets/(?P<versionptr>\d+)/bugs/active/$', jsonwrap(api.bugs)),
    (r'^snippet/(?P<version>\d+)/$', jsonwrap(api.snippet)),
    (r'^bugs/(?P<versionptr>\d+)/all/$', jsonwrap(api.bugs_all)),
    (r'^new/snippet/$', jsonwrap(api.new_snippet)),
    (r'^new/spec/$', jsonwrap(api.new_spec)),
    (r'^new/bug/$', jsonwrap(api.new_bug)),
    (r'^vote/$', jsonwrap(api.vote)),
    (r'^search/$', jsonwrap(api.search)),
    (r'^user/update/$', jsonwrap(api.user_update)),
)

urlpatterns = patterns('',
    (r'^/?$', views.home),
    (r'^api/', include(apipatterns)),
    (r'^spec/(?P<pk>\d+)/$', views.spec),
    (r'^(?P<pk>\d+)/$', views.snippet),
    (r'^search/$', include('haystack.urls')),
    (r'^new/$', views.new),
    (r'^profile/$', views.profile),
    (r'^static/(?P<path>[\w+\./-]+)$', django.views.static.serve, 
            { 'document_root': 'static'} ),
    (r'^openid/', include('django_openid_auth.urls')),
    (r'^logout/$', 'django.contrib.auth.views.logout', { 'next_page': '/' }),
)
