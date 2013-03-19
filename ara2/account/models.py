from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(max_length=120, blank=True)
    signature = models.CharField(max_length=3072, blank=True)
    self_introduction = models.CharField(max_length=3072, blank=True)
    default_language = models.CharField(max_length=15, blank=True)
    campus = models.CharField(max_length=45, blank=True)
    activated = models.IntegerField(null=True, blank=True)
    widget = models.IntegerField(null=True, blank=True)
    layout = models.IntegerField(null=True, blank=True)
    last_logout_time = models.DateTimeField(null=True, blank=True)
    last_login_ip = models.CharField(max_length=45, blank=True)
    is_sysop = models.IntegerField(null=True, blank=True)
    authentication_mode = models.IntegerField(null=True, blank=True)
    listing_mode = models.IntegerField(null=True, blank=True)
    activated_backup = models.IntegerField(null=True, blank=True)
    deleted = models.IntegerField(null=True, blank=True)


class LostPasswordToken(models.Model):
    user_id = models.ForeignKey(User, null=True, blank=True)
    code = models.CharField(max_length=75, blank=True)


class UserActivation(models.Model):
    user_id = models.ForeignKey(User, primary_key=True)
    activation_code = models.CharField(max_length=150, unique=True, blank=True)
    issued_date = models.DateTimeField(null=True, blank=True)


class Message(models.Model):
    from_id = models.ForeignKey(User, related_name='sent_messages')
    from_ip = models.CharField(max_length=45, blank=True)
    to_id = models.ForeignKey(User, related_name='received_messages')
    sent_time = models.DateTimeField(null=True, blank=True)
    message = models.CharField(max_length=3000, blank=True)
    received_deleted = models.IntegerField(null=True, blank=True)
    sent_deleted = models.IntegerField(null=True, blank=True)
    read_status = models.CharField(max_length=3, blank=True)
