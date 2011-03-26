from haystack.indexes import *
from haystack import site
from zoo.models import Spec

# TODO RealTimeSearchIndex will SUCK once things start getting going.
# Got to switch to Solr backend or a lazier indexing scheme.
class SpecIndex(SearchIndex):
    name = CharField(model_attr='name')
    summary = CharField(model_attr='summary')
    text = CharField(document=True, use_template=True)
    active = BooleanField(model_attr='version__active')

site.register(Spec, SpecIndex)
