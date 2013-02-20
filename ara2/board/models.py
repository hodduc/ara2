from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    title = models.CharField(max_length=600, blank=True)
    board_id = models.ForeignKey('Board', null=True, blank=True)
    heading_id = models.ForeignKey('BoardHeading', null=True, blank=True)
    content = models.TextField(blank=True)
    author_id = models.ForeignKey(User, null=True, blank=True)
    author_nickname = models.CharField(max_length=120, blank=True)
    author_ip = models.CharField(max_length=45, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    hit = models.IntegerField(null=True, blank=True)
    positive_vote = models.IntegerField(null=True, blank=True)
    negative_vote = models.IntegerField(null=True, blank=True)
    deleted = models.IntegerField(null=True, blank=True)
    root_id = models.ForeignKey('Article', related_name='articles', null=True, blank=True)
    parent_id = models.ForeignKey('Article', related_name='+', null=True, blank=True)
    reply_count = models.IntegerField()
    is_searchable = models.IntegerField()
    last_modified_date = models.DateTimeField(null=True, blank=True)
    destroyed = models.IntegerField(null=True, blank=True)
    last_reply_date = models.DateTimeField(null=True, blank=True)
    last_reply_id = models.IntegerField(null=True, blank=True)


class ArticleVoteStatus(models.Model):
    board_id = models.ForeignKey('Board')
    article_id = models.ForeignKey('Article')
    user_id = models.ForeignKey(User)


class BbsManager(models.Model):
    board_id = models.ForeignKey('Board', null=True, blank=True)
    manager_id = models.ForeignKey(User, null=True, blank=True)


class Blacklist(models.Model):
    user_id = models.ForeignKey(User, null=True, blank=True)
    blacklisted_user_id = models.ForeignKey(User, related_name='+', null=True, blank=True)
    blacklisted_date = models.DateTimeField(null=True, blank=True)
    last_modified_date = models.DateTimeField(null=True, blank=True)
    block_article = models.IntegerField(null=True, blank=True)
    block_message = models.IntegerField(null=True, blank=True)


class BoardHeading(models.Model):
    board_id = models.ForeignKey('Board', null=True, blank=True)
    heading = models.CharField(max_length=90, blank=True)


class BoardNotice(models.Model):
    article = models.ForeignKey('Article', primary_key=True)


class Board(models.Model):
    category_id = models.ForeignKey('Category', null=True, blank=True)
    board_name = models.CharField(max_length=90, unique=True, blank=True)
    board_alias = models.CharField(max_length=90, blank=True)
    board_description = models.CharField(max_length=900, blank=True)
    deleted = models.IntegerField(null=True, blank=True)
    read_only = models.IntegerField(null=True, blank=True)
    hide = models.IntegerField(null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    to_read_level = models.IntegerField(null=True, blank=True)
    to_write_level = models.IntegerField(null=True, blank=True)


class Category(models.Model):
    category_name = models.CharField(max_length=90, unique=True, blank=True)
    order = models.IntegerField(null=True, blank=True)


class File(models.Model):
    filename = models.CharField(max_length=600, blank=True)
    saved_filename = models.CharField(max_length=600, blank=True)
    filepath = models.TextField(blank=True)
    user_id = models.ForeignKey(User, null=True, blank=True)
    board_id = models.ForeignKey('Board', null=True, blank=True)
    article_id = models.ForeignKey('Article', null=True, blank=True)
    deleted = models.IntegerField(null=True, blank=True)


class ReadStatus(models.Model):
    user_id = models.ForeignKey(User, null=True, blank=True)
    article_id = models.ForeignKey('Article', null=True, blank=True)
    status = models.CharField(max_length=3, blank=True)


class ReadStatusOrg(models.Model):
    user_id = models.ForeignKey(User, null=True, blank=True)
    board_id = models.ForeignKey('Board', null=True, blank=True)
    read_status_data = models.TextField(blank=True)
    read_status_numbers = models.TextField(blank=True)
    read_status_markers = models.TextField(blank=True)


class ScrapStatus(models.Model):
    user_id = models.ForeignKey(User)
    article_id = models.ForeignKey('Article')


class SelectedBoard(models.Model):
    user_id = models.ForeignKey(User, null=True, blank=True)
    board_id = models.ForeignKey('Board', null=True, blank=True)
