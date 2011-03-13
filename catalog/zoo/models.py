from django.db import models

class Spec(models.Model):
    name = models.CharField(max_length=128)
    summary = models.TextField()
    spec = models.TextField()

class Snippet(models.Model):
    spec = models.ForeignKey(Spec)
    description = models.TextField()
    code = models.TextField()

class Test(models.Model):
    spec = models.ForeignKey(Spec)
    code = models.TextField()
