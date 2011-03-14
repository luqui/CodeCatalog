from django.db import models

class Spec(models.Model):
    name = models.CharField(max_length=128)
    summary = models.TextField()
    spec = models.TextField()

    def shortdesc(self):
        return "[spec] " + self.name + " - " + self.summary

    # don't think this belongs here
    def url(self):
        return '/spec/' + str(self.id) + '/'

class Snippet(models.Model):
    spec = models.ForeignKey(Spec)
    description = models.TextField()
    code = models.TextField()

    def shortdesc(self):
        return self.spec.name + " - " + self.spec.summary

    # don't think this belongs here
    def url(self):
        return '/' + str(self.id) + '/'

class Test(models.Model):
    spec = models.ForeignKey(Spec)
    code = models.TextField()
