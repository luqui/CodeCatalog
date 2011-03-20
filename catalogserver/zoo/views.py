from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from zoo.models import Spec, Snippet, Vote
from django.contrib.auth.decorators import login_required

# CodeCatalog Snippet http://codecatalog.net/14/
def linecount(s):
    return len(s.splitlines())
# End CodeCatalog Snippet

# CodeCatalog Snippet http://codecatalog.net/15/
def render(request, template, dictionary={}, context_instance=None, mimetype="text/html"):
    from django.shortcuts import render_to_response
    from django.template import RequestContext
    if context_instance == None:
        context_instance = RequestContext(request)
    return render_to_response(template, dictionary, context_instance=context_instance, mimetype=mimetype)
# End CodeCatalog Snippet

# CodeCatalog Snippet http://codecatalog.net/16/
def schwartzian_sort(list, metric, reverse=False):
    paired = [ (x, metric(x)) for x in list ]
    paired.sort(key=lambda x: x[1], reverse=reverse)
    return map(lambda x: x[0], paired)
# End CodeCatalog Snippet

def spec(request, pk):
    def metric(obj): return (obj.canon, obj.votes())

    obj = get_object_or_404(Spec, pk=pk)
    snippets = schwartzian_sort(obj.snippet_set.all(), metric, reverse=True)
    return render(request, 'zoo/spec.html', {'spec': obj, 'snippets': snippets})

def static(request, path):
    import re
    if re.match(r'\.\.', path):
        return HttpResponse()  # TODO error
    return render(request, 'static/' + path)

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
    return render(request, 'zoo/snippet.html', {'spec': obj.spec, 'snippet': obj})

def raw_snippet(request, pk):
    obj = get_object_or_404(Snippet, pk=pk)
    return render(request, 'zoo/rawcode.txt', {'snippet': obj}, mimetype="text/plain")

# CodeCatalog Snippet http://codecatalog.net/17/
def update_fields(fields, obj, post):
    edited = False
    for f in fields:
        if f in post:
            edited = True
            setattr(obj, f, post[f])
    if edited: obj.save()
# End CodeCatalog Snippet

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
        return render(request, 'zoo/new_for_spec.html', { 'spec': spec })
    code = request.POST['code'].strip()
    snippet = Snippet(spec=spec, code=code, date=datetime.now(), parent=None, canon=False)
    snippet.save()
    return HttpResponseRedirect('/' + str(snippet.id) + '/')

def new(request):
    if request.method != 'POST':
        return render(request, 'zoo/new.html')
    code = request.POST['code'].strip()
    name = detect_defined_function_name(code) or "unnamed"
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

# CodeCatalog Snippet http://codecatalog.net/18/
import re

def_rx = re.compile(r'^def\s+(\w+).*:', re.MULTILINE)
def detect_defined_function_name(code):
    match = def_rx.search(code)
    if match:
        return match.group(1)
    else:
        return None
# End CodeCatalog Snippet

