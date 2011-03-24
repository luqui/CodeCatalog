from haystack.indexes import *
from haystack import site
from zoo.models import Spec

class SpecIndex(SearchIndex):
    name = CharField(model_attr='name')
    summary = CharField(model_attr='summary')
    text = CharField(document=True, use_template=True)
    active = BooleanField(model_attr='version__active')

site.register(Spec, SpecIndex)
