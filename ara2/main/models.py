from django.db import models


class Banner(models.Model):
    content = models.TextField(blank=True)
    issued_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    valid = models.BooleanField(default=True)
    weight = models.IntegerField(null=True, blank=True)


class Visitor(models.Model):
    total = models.IntegerField(primary_key=True)
    today = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
