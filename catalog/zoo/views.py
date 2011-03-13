from django.shortcuts import render_to_response, get_object_or_404
from zoo.models import Spec, Snippet


def object_view(model, template):
    def view(request, pk):
        obj = get_object_or_404(model, pk=pk)
        return render_to_response(template, {str.lower(model.__name__): obj})
    return view

spec = object_view(Spec, 'zoo/spec.html')
snippet = object_view(Snippet, 'zoo/snippet.html')
