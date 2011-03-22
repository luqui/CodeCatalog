from django.db import models
from django.contrib.auth.models import User

class VersionID(models.Model):
    def votes(self):
        r = 0
        for vote in self.vote_set.all():
            r += vote.value
        return r

class Version(models.Model):
    timestamp = models.DateTimeField()
    user = models.ForeignKey(User, null=True)
    active = models.BooleanField()
    versionid = models.ForeignKey(VersionID)
    


class Spec(models.Model):
    version = models.OneToOneField(Version, primary_key=True)
    name = models.CharField(max_length=128)
    summary = models.TextField()
    spec = models.TextField()

    # don't think this belongs here
    def url(self):
        return '/spec/' + str(self.id) + '/'

class Snippet(models.Model):
    version = models.ForeignKey(Version, primary_key=True)
    code = models.TextField()
    language = models.TextField()
    versionid = models.ForeignKey(VersionID)


    # don't think this belongs here
    def url(self):
        return '/' + str(self.id) + '/'

class Vote(models.Model):
    user       = models.ForeignKey(User)
    version_id = models.ForeignKey(VersionID)
    table_type = models.IntegerField(choices = [
                            (0, 'Spec'),
                            (1, 'Snippet'),
                        ])
    value   = models.IntegerField()  # 1 or -1
    date    = models.DateTimeField()
