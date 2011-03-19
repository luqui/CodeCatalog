from django.db import models
from django.contrib.auth.models import User

class Spec(models.Model):
    name = models.CharField(max_length=128)
    summary = models.TextField()
    spec = models.TextField()
    parent = models.ForeignKey('self', related_name='child', null=True)

    # don't think this belongs here
    def url(self):
        return '/spec/' + str(self.id) + '/'

class Snippet(models.Model):
    spec = models.ForeignKey(Spec)
    code = models.TextField()
    date = models.DateField()
    parent = models.ForeignKey('self', related_name='child', null=True)
    canon = models.BooleanField()
    language = models.TextField(default='python')

    def votes(self):
        r = 0
        for vote in self.vote_set.all():
            r += vote.value
        return r

    # don't think this belongs here
    def url(self):
        return '/' + str(self.id) + '/'

class Vote(models.Model):
    user    = models.ForeignKey(User)
    snippet = models.ForeignKey(Snippet)
    value   = models.IntegerField()
    date    = models.DateField()
