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

def static(request, path):
    import re
    if re.match(r'\.\.', path):
        return HttpResponse()  # TODO error
    return render(request, 'static/' + path)

def snippet(request, pk):
    obj = get_object_or_404(Snippet, pk=pk)
    return render(request, 'zoo/snippet.html', {'spec': obj.spec, 'snippet': obj})

def raw_snippet(request, pk):
    obj = get_object_or_404(Snippet, pk=pk)
    return render(request, 'zoo/rawcode.txt', {'snippet': obj}, mimetype="text/plain")

def edit_spec(request, pk):
    s = get_object_or_404(Spec, pk=pk)
    update_fields(['name', 'summary', 'spec'], s, request.POST)
    return HttpResponse()

def branch_snippet(request, pk):
    s = get_object_or_404(Snippet, pk=pk)
    snippet = Snippet(spec=s.spec, code=request.POST['code'], date=datetime.now(), parent=s, canon=False, language=request.POST['language'])
    snippet.save()
    return HttpResponse()

def delete_snippet(request, pk):
    s = get_object_or_404(Snippet, pk=pk)
    for c in s.child.all():
        c.parent = s.parent
        c.save()
    s.delete()
    return HttpResponse()

def new(request):
    if request.method != 'POST':
        return render(request, 'zoo/new.html')
    code = request.POST['code'].strip()
    name = detect_defined_function_name(code) or "unnamed"
    spec = Spec(name=name, parent=None)
    spec.save()
    snippet = Snippet(spec=spec, code=code, date=datetime.now(), parent=None, canon=True, language=request.POST['language'])
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

