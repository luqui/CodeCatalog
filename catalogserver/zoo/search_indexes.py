from haystack.indexes import *
from haystack import site
from zoo.models import Spec, VersionPtr

class SpecIndex(RealTimeSearchIndex):
    name = CharField()
    summary = CharField()
    spec = CharField()
    versionptrid = IntegerField()
    text_gram = CharField(document=True, use_template=True)
    text = CharField(use_template=True)
    alltext = CharField(use_template=True)

    def get_queryset(self):
        return VersionPtr.objects.filter(
            type=VersionPtr.PTRTYPE_TO_ID['Spec'],
            version__active=True,
            version__spec__status=Spec.STATUS_TO_ID['Open'])

    def should_update(self, obj, **kwargs):
        specptr = obj.type == VersionPtr.PTRTYPE_TO_ID['Spec']
        if specptr:
            active = obj.active_spec()
            if active and obj.active_spec().status != Spec.STATUS_TO_ID['Open']:
                self.remove_object(obj)
                return False
        return specptr        

    def prepare_name(self, obj):
        active = obj.active_spec()
        return active and active.name

    def prepare_summary(self, obj):
        active = obj.active_spec()
        return active and active.summary
    
    def prepare_spec(self, obj):
        active = obj.active_spec()
        return active and active.spec

    def prepare_versionptrid(self, obj):
        return obj.id

site.register(VersionPtr, SpecIndex)
