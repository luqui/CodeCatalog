from djapian import space, Indexer, CompositeIndexer

from zoo.models import *

class SpecIndexer(Indexer):
    fields = ['name', 'summary', 'spec']

space.add_index(Spec, SpecIndexer, attach_as='indexer')

class SnippetIndexer(Indexer):
    fields = ['description', 'code']

space.add_index(Snippet, SnippetIndexer, attach_as='indexer')

complete_indexer = CompositeIndexer(Spec.indexer, Snippet.indexer)
