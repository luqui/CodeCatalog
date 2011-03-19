from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from zoo.models import Spec, Snippet
import re

def linecount(s): return len(s.splitlines())

def spec(request, pk):
    obj = get_object_or_404(Spec, pk=pk)
    snippets = [ 
        { 'code': o.code, 'lines': min(10, linecount(o.code)), 'id': o.id } 
            for o in obj.snippet_set.all() ]
    return render_to_response('zoo/spec.html', {'spec': obj, 'snippets': snippets}, context_instance=RequestContext(request))

def snippet(request, pk):
    obj = get_object_or_404(Snippet, pk=pk)
    return render_to_response('zoo/snippet.html', {'spec': obj.spec, 'snippet': obj}, context_instance=RequestContext(request))

def raw_snippet(request, pk):
    obj = get_object_or_404(Snippet, pk=pk)
    return render_to_response('zoo/rawcode.txt', {'snippet': obj}, mimetype="text/plain", context_instance=RequestContext(request))

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

def branch_snippet(request, pk):
    s = get_object_or_404(Snippet, pk=pk)
    snippet = Snippet(spec=s.spec, code=request.POST['code'], date=datetime.now(), parent=s)
    snippet.save()
    return HttpResponse()

def delete_snippet(request, pk):
    s = get_object_or_404(Snippet, pk=pk)
    for c in s.child.all():
        c.parent = s.parent
        c.save()
    s.delete()
    return HttpResponse()

def new_for_spec(request, pk):
    spec = get_object_or_404(Spec, pk=pk)
    if request.method != 'POST':
        return render_to_response('zoo/new_for_spec.html', { 'spec': spec }, context_instance=RequestContext(request))
    code = request.POST['code'].strip()
    snippet = Snippet(spec=spec, code=code, date=datetime.now(), parent=None)
    snippet.save()
    return HttpResponseRedirect('/' + str(snippet.id) + '/')

def new(request):
    if request.method != 'POST':
        return render_to_response('zoo/new.html', context_instance=RequestContext(request))
    code = request.POST['code'].strip()
    name = detect_spec_name(code)
    spec = Spec(name=name, parent=None)
    spec.save()
    snippet = Snippet(spec=spec, code=code, date=datetime.now(), parent=None)
    snippet.save()
    return HttpResponseRedirect('/' + str(snippet.id) + '/')

def_rx = re.compile(r'^def\s+(\w+).*:', re.MULTILINE)
def detect_spec_name(code):
    match = def_rx.search(code)
    if match:
        return match.group(1)
    else:
        return "unnamed"
