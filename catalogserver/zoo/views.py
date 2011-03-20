from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from zoo.models import Spec, Snippet, Vote
from django.contrib.auth.decorators import login_required
import re

def linecount(s): return len(s.splitlines())

def spec(request, pk):
    obj = get_object_or_404(Spec, pk=pk)
    snippets = []
    for o in obj.snippet_set.all():
        votes = o.votes()
        snippets.append({ 'code': o.code, 
                          'lines': min(10, linecount(o.code)), 
                          'id': o.id, 
                          'canon': o.canon,
                          'votes': votes,
                          'sortkey': (o.canon, votes) })
    snippets.sort(key=lambda x: x['sortkey'], reverse=True)
    return render_to_response('zoo/spec.html', {'spec': obj, 'snippets': snippets}, context_instance=RequestContext(request))

def static(request, path):
    if re.match(r'\.\.', path):
        return HttpResponse()  # TODO error
    return render_to_response('static/' + path)

@login_required
def vote_snippet(request, val, pk):
    snippet = get_object_or_404(Snippet, pk=pk)
    val = int(val)
    pvotes = Vote.objects.filter(user__exact=request.user, snippet__exact=snippet).all()
    for v in pvotes:
        v.delete()
    if val != 0:
        v = Vote(user=request.user, snippet=snippet, value=val, date=datetime.now())
        v.save()
    return HttpResponse()

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
    snippet = Snippet(spec=s.spec, code=request.POST['code'], date=datetime.now(), parent=s, canon=False)
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
    snippet = Snippet(spec=spec, code=code, date=datetime.now(), parent=None, canon=False)
    snippet.save()
    return HttpResponseRedirect('/' + str(snippet.id) + '/')

def new(request):
    if request.method != 'POST':
        return render_to_response('zoo/new.html', context_instance=RequestContext(request))
    code = request.POST['code'].strip()
    name = detect_spec_name(code)
    spec = Spec(name=name, parent=None)
    spec.save()
    snippet = Snippet(spec=spec, code=code, date=datetime.now(), parent=None, canon=True)
    snippet.save()
    return HttpResponseRedirect('/spec/' + str(spec.id) + '/')

def set_canon(request, pk):
    s = get_object_or_404(Snippet, pk=pk)
    current_canon = Snippet.objects.filter(spec__exact=s.spec, language__exact=s.language, canon__exact=True)
    # TODO race condition
    for i in current_canon:
        i.canon = False
        i.save()
    s.canon = True
    s.save()
    return HttpResponse()

def_rx = re.compile(r'^def\s+(\w+).*:', re.MULTILINE)
def detect_spec_name(code):
    match = def_rx.search(code)
    if match:
        return match.group(1)
    else:
        return "unnamed"
