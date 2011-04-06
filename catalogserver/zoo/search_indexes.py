from haystack.indexes import *
from haystack import site
from zoo.models import Spec, VersionPtr

class SpecIndex(RealTimeSearchIndex):
    name = CharField()
    summary = CharField()
    versionptrid = IntegerField()
    text = CharField(document=True, use_template=True)

    def get_queryset(self):
        return VersionPtr.objects.filter(type=VersionPtr.PTRTYPE_TO_ID['Spec'])

    def should_update(self, obj, **kwargs):
        return obj.type == VersionPtr.PTRTYPE_TO_ID['Spec']

    def prepare_name(self, obj):
        active = obj.active_spec()
        return active and active.name

    def prepare_summary(self, obj):
        active = obj.active_spec()
        return active and active.summary

    def prepare_versionptrid(self, obj):
        return obj.id

site.register(VersionPtr, SpecIndex)
