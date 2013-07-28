# -*- coding: utf-8 -*-
from django.db import models
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        app_label = 'ara2'

    LANGUAGE_CHOICES = (
        # ISO 639-1 language code
        ('ko', u'한국어'), # default
        ('en', u'English'),
    )

    CAMPUS_CHOICES = (
        ('seoul', u'Seoul'),
        ('daejeon', u'Daejeon'), # default
    )

    AUTH_MODES = (
        (0, 'not auth'), # default
        (1, 'mail with non @kaist'),
        (2, 'mail with @kaist'),
        (3, 'portal'),
    )

    LISTING_MODES = (
        (0, 'ROOT_ID'), # default
        (1, 'LAST_REPLY_DATE'),
    )

    nickname = models.CharField(max_length=120)
    signature = models.CharField(max_length=3072, blank=True)
    self_introduction = models.CharField(max_length=3072, blank=True)
    default_language = models.CharField(max_length=15, choices=LANGUAGE_CHOICES, default='ko')
    campus = models.CharField(max_length=45, choices=CAMPUS_CHOICES)
    last_logout_time = models.DateTimeField(null=True, blank=True)
    last_login_ip = models.CharField(max_length=45, blank=True)
    authentication_mode = models.IntegerField(choices=AUTH_MODES, default=0)
    listing_mode = models.IntegerField(choices=LISTING_MODES, default=0)
    activated_backup = models.IntegerField(null=True, blank=True)
    deleted = models.BooleanField()


class LostPasswordToken(models.Model):
    class Meta:
        app_label = 'ara2'

    user = models.ForeignKey(User)
    code = models.CharField(max_length=75)


class UserActivation(models.Model):
    class Meta:
        app_label = 'ara2'

    user = models.ForeignKey(User, primary_key=True)
    activation_code = models.CharField(max_length=150)
    issued_date = models.DateTimeField() # XXX: auto_now_add


class Message(models.Model):
    class Meta:
        app_label = 'ara2'

    from_user = models.ForeignKey(User, related_name='sent_messages')
    from_ip = models.CharField(max_length=45, blank=True)
    to_user = models.ForeignKey(User, related_name='received_messages')
    sent_time = models.DateTimeField() # XXX: auto_now_add
    message = models.CharField(max_length=3000, blank=True)
    received_deleted = models.BooleanField()
    sent_deleted = models.BooleanField()
    read_status = models.CharField(max_length=3, blank=True)
