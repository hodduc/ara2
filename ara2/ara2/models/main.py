# -*- coding: utf-8 -*-
from django.db import models
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser


class Banner(models.Model):
    class Meta:
        app_label = 'ara2'

    content = models.TextField(blank=True)
    issued_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    valid = models.BooleanField(default=True)
    weight = models.IntegerField(null=True, blank=True)


class Visitor(models.Model):
    class Meta:
        app_label = 'ara2'

    total = models.IntegerField(primary_key=True)
    today = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
