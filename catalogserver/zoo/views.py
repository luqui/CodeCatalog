from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from datetime import datetime
from zoo.models import *
from django.contrib.auth.decorators import login_required
from zoo import api

def render(request, template, dictionary={}, context_instance=None, mimetype="text/html"):
    from django.shortcuts import render_to_response
    from django.template import RequestContext
    if context_instance == None:
        context_instance = RequestContext(request)
    return render_to_response(template, dictionary, context_instance=context_instance, mimetype=mimetype)

def latest(request, versionptr):
    vptr = get_object_or_404(VersionPtr, pk=versionptr)
    typ = VersionPtr.ID_TO_PTRTYPE[vptr.type]
    if typ == 'Snippet':
        return render_snippet(request, api.snippets_active(request, versionptr))
    elif typ == 'Spec':
        return render_spec(request, api.specs_active(request, versionptr))
    elif typ == 'BugReport':
        raise Http404()  # TODO bug page

def version(request, versionptr, version):
    vptr = get_object_or_404(VersionPtr, pk=versionptr)
    typ = VersionPtr.ID_TO_PTRTYPE[vptr.type]
    if typ == 'Snippet':
        snip = api.snippet(request, version)
        if snip['versionptr'] != int(versionptr): raise Http404()
        return render_snippet(request, snip)
    elif typ == 'Spec':
        spec = api.spec(request, version)
        if spec['versionptr'] != int(versionptr): raise Http404()
        return render_spec(request, spec)
    elif typ == 'BugReport':
        raise Http404()  # TODO bug page

def render_spec(request, spec):
    snippets = api.specs_snippets_active(request, spec['versionptr'])
    return render(request, 'zoo/spec.html', {'spec': spec, 'snippets': snippets})

def render_snippet(request, snippet):
    spec = api.specs_active(request, snippet['spec_versionptr'])
    return render(request, 'zoo/snippet.html', {'spec': spec, 'snippets': [snippet] })

def static(request, path):
    import re
    if re.match(r'\.\.', path):
        return HttpResponse()  # TODO error
    return render(request, 'static/' + path)

def template(tmpl):
    def view(request):
        return render(request, tmpl)
    return view

new = template('zoo/new.html')

def home(request):
    latest = Spec.objects.filter(version__active=True).order_by('-version__timestamp')
    return render(request, 'zoo/home.html', {'specs': latest[0:10]})

faq = template('zoo/faq.html')

tools = template('zoo/tools.html')

@login_required
def profile(request):
    if request.method == 'POST':
        api.user_update(request)
    request.user = User.objects.get(id=request.user.id)
    return render(request, 'zoo/profile.html')
