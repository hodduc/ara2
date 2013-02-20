from django.db import models


class Banner(models.Model):
    content = models.TextField(blank=True)
    issued_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    valid = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)


class Link(models.Model):
    link_name = models.CharField(max_length=90, unique=True, blank=True)
    link_description = models.CharField(max_length=900, blank=True)
    link_url = models.CharField(max_length=300, blank=True)
    ishidden = models.IntegerField(null=True, blank=True)
    deleted = models.IntegerField(null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)


class Visitor(models.Model):
    total = models.IntegerField(primary_key=True)
    today = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)


class Welcome(models.Model):
    content = models.TextField(blank=True)
    issued_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    valid = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)

