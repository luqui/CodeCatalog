from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from zoo.models import *

def get_snippet(request, pk):
    obj = get_object_or_404(Snippet, pk=pk)
    return {
        'code': obj.code,
        'votes': obj.votes(),
    }
