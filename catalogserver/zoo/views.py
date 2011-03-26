from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from zoo.models import Spec, Snippet, Vote
from django.contrib.auth.decorators import login_required
from zoo import api

def render(request, template, dictionary={}, context_instance=None, mimetype="text/html"):
    from django.shortcuts import render_to_response
    from django.template import RequestContext
    if context_instance == None:
        context_instance = RequestContext(request)
    return render_to_response(template, dictionary, context_instance=context_instance, mimetype=mimetype)

def spec(request, pk):
    def metric(obj): return (obj.canon, obj.votes())
    spec = api.specs_active(request, pk)
    snippets = api.specs_snippets_active(request, pk)
    return render(request, 'zoo/spec.html', {'spec': spec, 'snippets': snippets})

def snippet(request, pk):
    obj = get_object_or_404(Snippet, pk=pk)
    snippet = api.snippet(request, pk)
    spec = api.specs_active(request, snippet['spec_versionptr'])
    return render(request, 'zoo/spec.html', {'spec': spec, 'snippets': [snippet] })

def static(request, path):
    import re
    if re.match(r'\.\.', path):
        return HttpResponse()  # TODO error
    return render(request, 'static/' + path)

def new(request):
    return render(request, 'zoo/new.html')

def home(request):
    latest = Spec.objects.filter(version__active=True).order_by('-version__timestamp')
    return render(request, 'zoo/home.html', {'specs': latest[0:10]})
