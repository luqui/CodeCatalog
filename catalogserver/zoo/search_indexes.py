from haystack.indexes import *
from haystack import site
from zoo.models import Spec

class SpecIndex(RealTimeSearchIndex):
    name = CharField(model_attr='name')
    summary = CharField(model_attr='summary')
    text = CharField(document=True, use_template=True)
    active = BooleanField(model_attr='version__active')

    def get_queryset(self):
        return Spec.objects.filter(version__active=True)

site.register(Spec, SpecIndex)
