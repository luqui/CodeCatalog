from django.db import models
from django.contrib.auth.models import User

# CodeCatalog Snippet http://codecatalog.net/45/134/
def dict_inverse(dictionary):
    r = {}
    for k,v in dictionary.items():
        if v in r:
            raise ValueError(
                """Dictionary given to dict_inverse is not one-to-one.  
                   Duplicate value: {value}
                   Mapped to by: {key1} and {key2}""".format(value=v, key1=r[v], key2=k))
        r[v] = k
    return r
# End CodeCatalog Snippet

class VersionPtr(models.Model):
    ID_TO_PTRTYPE = {
        0: 'Spec',
        1: 'Snippet',
        2: 'BugReport',
    }
    PTRTYPE_TO_ID = dict_inverse(ID_TO_PTRTYPE)
    type = models.IntegerField(choices=ID_TO_PTRTYPE.items())

    def active_version(self):
        return Version.objects.filter(versionptr=self, active=True)

    def active_spec(self):
        specset = Spec.objects.filter(version = self.active_version())
        if specset.exists():
            return specset[0]
        else:
            return None

class Version(models.Model):
    timestamp  = models.DateTimeField()
    user       = models.ForeignKey(User, null=True)
    approved   = models.BooleanField()
    active     = models.BooleanField()    # cache field that always marks the latest approved version
    versionptr = models.ForeignKey(VersionPtr)
    comment    = models.TextField()

class Spec(models.Model):
    ID_TO_STATUS = {
        0: 'Open',
        1: 'Deprecated',
    }
    STATUS_TO_ID = dict_inverse(ID_TO_STATUS)

    version = models.OneToOneField(Version, primary_key=True)
    name    = models.CharField(max_length=64)
    summary = models.TextField()
    spec    = models.TextField()
    status  = models.IntegerField(choices=ID_TO_STATUS.items())

class Snippet(models.Model):
    version         = models.OneToOneField(Version, primary_key=True)
    code            = models.TextField()
    language        = models.CharField(max_length=32)
    spec_versionptr = models.ForeignKey(VersionPtr)

class Dependency(models.Model):
    snippet = models.ForeignKey(Snippet)
    target  = models.ForeignKey(VersionPtr)  # points to a spec versionptr

class BugReport(models.Model):
    ID_TO_STATUS = { 
        0: 'Open',
        1: 'Resolved',
        2: 'Closed',
    }
    STATUS_TO_ID = dict_inverse(ID_TO_STATUS)

    version = models.OneToOneField(Version, primary_key=True)
    target_versionptr = models.ForeignKey(VersionPtr)
    title = models.TextField()
    status = models.IntegerField(choices=ID_TO_STATUS.items())

class Following(models.Model):
    follower = models.ForeignKey(User)
    followed = models.ForeignKey(VersionPtr)
    new_events = models.BooleanField()
    last_check = models.DateTimeField()
