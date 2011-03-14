from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse
from zoo.models import Spec, Snippet
from zoo.index import complete_indexer
import pprint

def object_view(model, template):
    def view(request, pk):
        obj = get_object_or_404(model, pk=pk)
        return render_to_response(template, {str.lower(model.__name__): obj}, context_instance=RequestContext(request))
    return view

spec = object_view(Spec, 'zoo/spec.html')
snippet = object_view(Snippet, 'zoo/snippet.html')

def search(request):
    if 'q' in request.GET:
        results = complete_indexer.search(request.GET['q']).prefetch()
        return render_to_response('zoo/searchresult.html', { 'results': results }, context_instance=RequestContext(request))
    else:
        return render_to_response('zoo/search.html', context_instance=RequestContext(request))

def editspec(request, pk):
    print pprint.pprint(request.POST)
    s = get_object_or_404(Spec, pk=pk)
    fields = [ 'name', 'summary', 'spec' ]
    for f in fields:
        print "Checking " + f + " in request"
        if f in request.POST:
            print "Setting attr " + str(s.id) + "[" + f + "] = " + request.POST[f]
            setattr(s, f, request.POST[f])
    s.save()
    return HttpResponse()
