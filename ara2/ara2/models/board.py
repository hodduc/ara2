# -*- coding: utf-8 -*-
from django.db import models
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser

from .account import User


class Article(models.Model):
    class Meta:
        app_label = 'ara2'

    # Field from users
    title = models.CharField(max_length=600, blank=True)
    content = models.TextField(blank=True)
    date = models.DateTimeField(null=True, blank=True)

    # Field for categorization
    board = models.ForeignKey('Board', null=True, blank=True)
    heading = models.ForeignKey('BoardHeading', null=True, blank=True)

    # Field about author
    author = models.ForeignKey(User, null=True, blank=True)
    author_nickname = models.CharField(max_length=120, blank=True)
    author_ip = models.CharField(max_length=45, blank=True)

    # Field about statistics
    hit = models.IntegerField(null=True, blank=True)
    positive_vote = models.IntegerField(null=True, blank=True)
    negative_vote = models.IntegerField(null=True, blank=True)

    # Flags
    deleted = models.BooleanField()
    destroyed = models.BooleanField()
    is_searchable = models.BooleanField(default=True)

    # Field about relationship with other articles
    root = models.ForeignKey('Article', related_name='articles', null=True, blank=True)
    parent = models.ForeignKey('Article', related_name='+', null=True, blank=True)
    reply_count = models.IntegerField()
    last_modified_date = models.DateTimeField(null=True, blank=True)
    last_reply_date = models.DateTimeField(null=True, blank=True)
    last_reply_id = models.IntegerField(null=True, blank=True)


class ArticleVoteStatus(models.Model):
    class Meta:
        app_label = 'ara2'

    article = models.ForeignKey('Article')
    user = models.ForeignKey(User)


class BbsManager(models.Model):
    class Meta:
        app_label = 'ara2'

    board = models.ForeignKey('Board', null=True, blank=True)
    manager = models.ForeignKey(User, null=True, blank=True)


class Blacklist(models.Model):
    class Meta:
        app_label = 'ara2'

    user = models.ForeignKey(User, null=True, blank=True)
    blacklisted_user = models.ForeignKey(User, related_name='+', null=True, blank=True)
    blacklisted_date = models.DateTimeField(null=True, blank=True)
    last_modified_date = models.DateTimeField(null=True, blank=True)
    block_article = models.BooleanField()
    block_message = models.BooleanField()


class BoardHeading(models.Model):
    class Meta:
        app_label = 'ara2'

    board = models.ForeignKey('Board', null=True, blank=True)
    heading = models.CharField(max_length=90, blank=True)


class BoardNotice(models.Model):
    class Meta:
        app_label = 'ara2'

    article = models.ForeignKey('Article', primary_key=True)


class Board(models.Model):
    class Meta:
        app_label = 'ara2'

    TYPE_CHOICES = (
            (0, 'Board'),
            (1, 'Gallery'),
            (2, 'Anonymous Board'),
    )

    category = models.ForeignKey('Category', null=True, blank=True)
    board_name = models.CharField(max_length=90, unique=True, blank=True)
    board_alias = models.CharField(max_length=90, blank=True)
    board_description = models.CharField(max_length=900, blank=True)
    deleted = models.BooleanField()
    read_only = models.BooleanField()
    hide = models.BooleanField()
    order = models.IntegerField(null=True, blank=True)
    type = models.IntegerField(null=True, blank=True, choices=TYPE_CHOICES)
    to_read_level = models.IntegerField(null=True, blank=True)
    to_write_level = models.IntegerField(null=True, blank=True)


class Category(models.Model):
    class Meta:
        app_label = 'ara2'

    category_name = models.CharField(max_length=90, unique=True, blank=True)
    order = models.IntegerField(null=True, blank=True)


class File(models.Model):
    class Meta:
        app_label = 'ara2'

    filename = models.CharField(max_length=600, blank=True)
    saved_filename = models.CharField(max_length=600, blank=True)
    filepath = models.TextField(blank=True)
    user = models.ForeignKey(User, null=True, blank=True)
    board = models.ForeignKey('Board', null=True, blank=True)
    article = models.ForeignKey('Article', null=True, blank=True)
    deleted = models.BooleanField()


class ScrapStatus(models.Model):
    class Meta:
        app_label = 'ara2'

    user = models.ForeignKey(User)
    article = models.ForeignKey('Article')


class SelectedBoard(models.Model):
    class Meta:
        app_label = 'ara2'

    user = models.ForeignKey(User, null=True, blank=True)
    board = models.ForeignKey('Board', null=True, blank=True)
