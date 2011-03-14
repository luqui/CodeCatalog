from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from zoo.models import Spec, Snippet
from zoo.index import complete_indexer

def object_view(model, template):
    def view(request, pk):
        obj = get_object_or_404(model, pk=pk)
        return render_to_response(template, {str.lower(model.__name__): obj})
    return view

spec = object_view(Spec, 'zoo/spec.html')
snippet = object_view(Snippet, 'zoo/snippet.html')

def search(request):
    if 'q' in request.POST:
        results = complete_indexer.search(request.POST['q']).prefetch()
        return render_to_response('zoo/searchresult.html', { 'results': results }, context_instance=RequestContext(request))
    else:
        return render_to_response('zoo/search.html', context_instance=RequestContext(request))
