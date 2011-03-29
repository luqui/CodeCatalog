from django.db import models
from django.contrib.auth.models import User

class VersionPtr(models.Model):
    votes = models.IntegerField(default=0)

class Version(models.Model):
    timestamp  = models.DateTimeField()
    user       = models.ForeignKey(User, null=True)
    approved   = models.BooleanField()
    active     = models.BooleanField()    # cache field that always marks the latest approved version
    versionptr = models.ForeignKey(VersionPtr)
    comment    = models.TextField()

class Spec(models.Model):
    version = models.OneToOneField(Version, primary_key=True)
    name    = models.CharField(max_length=64)
    summary = models.TextField()
    spec    = models.TextField()

class Snippet(models.Model):
    version         = models.OneToOneField(Version, primary_key=True)
    code            = models.TextField()
    language        = models.CharField(max_length=32)
    spec_versionptr = models.ForeignKey(VersionPtr)

class Dependency(models.Model):
    snippet = models.ForeignKey(Snippet)
    target  = models.ForeignKey(VersionPtr)  # points to a spec versionptr

class Vote(models.Model):
    user       = models.ForeignKey(User)
    versionptr = models.ForeignKey(VersionPtr)
    value      = models.IntegerField()  # 1 or -1
    timestamp  = models.DateTimeField()

# CodeCatalog Snippet http://codecatalog.net/134/
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
