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
    (r'^specs/(?P<versionptr>\d+)/assemble/$', jsonwrap(api.specs_assemble)),
    (r'^specs/(?P<versionptr>\d+)/bugs/active/$', jsonwrap(api.bugs)),
    (r'^spec/(?P<version>\d+)/$', jsonwrap(api.spec)),
    (r'^snippets/(?P<versionptr>\d+)/active/$', jsonwrap(api.snippets_active)),
    (r'^snippets/(?P<versionptr>\d+)/all/$', jsonwrap(api.snippets_all)),
    (r'^snippets/(?P<versionptr>\d+)/bugs/active/$', jsonwrap(api.bugs)),
    (r'^snippet/(?P<version>\d+)/$', jsonwrap(api.snippet)),
    (r'^snippet/(?P<version>\d+)/assemble/', jsonwrap(api.snippet_assemble)),
    (r'^bugs/(?P<versionptr>\d+)/all/$', jsonwrap(api.bugs_all)),
    (r'^bug/(?P<version>\d+)/', jsonwrap(api.bug)),
    (r'^new/snippet/$', jsonwrap(api.new_snippet)),
    (r'^new/spec/$', jsonwrap(api.new_spec)),
    (r'^new/bug/$', jsonwrap(api.new_bug)),
    (r'^search/$', jsonwrap(api.search)),
    (r'^user/update/$', jsonwrap(api.user_update)),
    (r'^user/events/check/$', jsonwrap(api.user_events_check)),
    (r'^user/events/new/$', jsonwrap(api.user_events_new)),
    (r'^user/events/mark_viewed/$', jsonwrap(api.user_events_mark_viewed)),
    (r'^user/make_api_key/$', jsonwrap(api.user_make_api_key)),
    (r'^orm/$', jsonwrap(api.orm)),
)

urlpatterns = patterns('',
    (r'^/?$', views.home),
    (r'^api/', include(apipatterns)),
    (r'^(?P<versionptr>\d+)/$', views.latest),
    (r'^(?P<versionptr>\d+)/(?P<version>\d+)/$', views.version),
    (r'^search/$', include('haystack.urls')),
    (r'^new/$', views.new),
    (r'^profile/$', views.profile),
    (r'^faq/$', views.faq),
    (r'^tools/$', views.tools),
    (r'^(?P<path>favicon.ico)/?$', django.views.static.serve, { 'document_root': 'static' }),
    (r'^static/(?P<path>[\w+\./-]+)$', django.views.static.serve, 
            { 'document_root': 'static'} ),
    url(r'^openid/login/$', 'django_openid_auth.views.login_begin', { 'template_name': 'registration/login.html' }, name='openid-login'),
    url(r'^openid/complete/$', 'django_openid_auth.views.login_complete', name='openid-complete'),
    (r'^logout/$', 'django.contrib.auth.views.logout'),
)
