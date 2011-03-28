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

class Comment(models.Model):
    user       = models.ForeignKey(User)
    versionptr = models.ForeignKey(VersionPtr)
    text       = models.TextField()
    timestamp  = models.DateTimeField()
