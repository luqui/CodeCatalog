from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from zoo.models import Spec, Snippet
from zoo.index import complete_indexer
import re

def spec(request, pk):
    obj = get_object_or_404(Spec, pk=pk)
    return render_to_response('zoo/spec.html', {'spec': obj}, context_instance=RequestContext(request))

def snippet(request, pk):
    obj = get_object_or_404(Snippet, pk=pk)
    return render_to_response('zoo/snippet.html', {'spec': obj.spec, 'snippet': obj}, context_instance=RequestContext(request))

def search(request):
    if 'q' in request.GET:
        results = complete_indexer.search(request.GET['q']).prefetch()
        return render_to_response('zoo/searchresult.html', { 'results': results }, context_instance=RequestContext(request))
    else:
        return render_to_response('zoo/search.html', context_instance=RequestContext(request))

def update_fields(fields, obj, post):
    edited = False
    for f in fields:
        if f in post:
            edited = True
            setattr(obj, f, post[f])
    if edited: obj.save()

def edit_spec(request, pk):
    s = get_object_or_404(Spec, pk=pk)
    update_fields(['name', 'summary', 'spec'], s, request.POST)
    return HttpResponse()

def edit_snippet(request, pk):
    s = get_object_or_404(Snippet, pk=pk)
    edit_spec(request, s.spec.id)
    update_fields(['description', 'code'], s, request.POST)
    return HttpResponse()

def new(request):
    if request.method != 'POST':
        return render_to_response('zoo/new.html', context_instance=RequestContext(request))
    code = request.POST['code']
    name = detect_spec_name(code)
    spec = Spec(name=name)
    spec.save()
    snippet = Snippet(spec=spec, code=code)
    snippet.save()
    return HttpResponseRedirect('/' + str(snippet.id) + '/')

def_rx = re.compile(r'^def\s+(\w+).*:', re.MULTILINE)
def detect_spec_name(code):
    match = def_rx.search(code)
    if match:
        return match.group(1)
    else:
        return "unnamed"
