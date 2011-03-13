from django.db import models

class Spec(models.Model):
    name = models.CharField(max_length=128)
    summary = models.TextField()
    spec = models.TextField()

    def shortdesc(self):
        return self.name + " - " + self.summary

class Snippet(models.Model):
    spec = models.ForeignKey(Spec)
    description = models.TextField()
    code = models.TextField()

    def shortdesc(self):
        return self.spec.shortdesc()

class Test(models.Model):
    spec = models.ForeignKey(Spec)
    code = models.TextField()
