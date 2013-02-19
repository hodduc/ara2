#-*- coding: utf-8 -*-
from django.db import models


class AraraSession(models.Model):
    session_key = models.CharField(max_length=120, primary_key=True)
    session_data = models.TextField(blank=True)
    expire_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = u'arara_session'


class ArticleVoteStatus(models.Model):
    board_id = models.ForeignKey('Board')
    article_id = models.ForeignKey('Article')
    user_id = models.ForeignKey('User')

    class Meta:
        db_table = u'article_vote_status'


class Article(models.Model):
    title = models.CharField(max_length=600, blank=True)
    board_id = models.ForeignKey('Board', null=True, blank=True)
    heading_id = models.ForeignKey('BoardHeading', null=True, blank=True)
    content = models.TextField(blank=True)
    author_id = models.ForeignKey('User', null=True, blank=True)
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

    class Meta:
        db_table = u'articles'


class Banner(models.Model):
    content = models.TextField(blank=True)
    issued_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    valid = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = u'banners'


class BbsManager(models.Model):
    board_id = models.ForeignKey('Board', null=True, blank=True)
    manager_id = models.ForeignKey('User', null=True, blank=True)

    class Meta:
        db_table = u'bbs_managers'


class Blacklist(models.Model):
    user_id = models.ForeignKey('User', null=True, blank=True)
    blacklisted_user_id = models.ForeignKey('User', related_name='+', null=True, blank=True)
    blacklisted_date = models.DateTimeField(null=True, blank=True)
    last_modified_date = models.DateTimeField(null=True, blank=True)
    block_article = models.IntegerField(null=True, blank=True)
    block_message = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = u'blacklists'


class BoardHeading(models.Model):
    board_id = models.ForeignKey('Board', null=True, blank=True)
    heading = models.CharField(max_length=90, blank=True)

    class Meta:
        db_table = u'board_headings'


class BoardNotice(models.Model):
    article = models.ForeignKey('Article', primary_key=True)

    class Meta:
        db_table = u'board_notice'


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

    class Meta:
        db_table = u'boards'


class Category(models.Model):
    category_name = models.CharField(max_length=90, unique=True, blank=True)
    order = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = u'categories'


class File(models.Model):
    filename = models.CharField(max_length=600, blank=True)
    saved_filename = models.CharField(max_length=600, blank=True)
    filepath = models.TextField(blank=True)
    user_id = models.ForeignKey('User', null=True, blank=True)
    board_id = models.ForeignKey('Board', null=True, blank=True)
    article_id = models.ForeignKey('Article', null=True, blank=True)
    deleted = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = u'files'


class Link(models.Model):
    link_name = models.CharField(max_length=90, unique=True, blank=True)
    link_description = models.CharField(max_length=900, blank=True)
    link_url = models.CharField(max_length=300, blank=True)
    ishidden = models.IntegerField(null=True, blank=True)
    deleted = models.IntegerField(null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = u'links'


class LoginSession(models.Model):
    session_key = models.CharField(max_length=120, primary_key=True)
    session_data = models.TextField(blank=True)
    expire_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = u'login_sessions'


class LostPasswordToken(models.Model):
    user_id = models.ForeignKey('User', null=True, blank=True)
    code = models.CharField(max_length=75, blank=True)

    class Meta:
        db_table = u'lost_password_token'


class Message(models.Model):
    from_id = models.ForeignKey('User', related_name='sent_messages')
    from_ip = models.CharField(max_length=45, blank=True)
    to_id = models.ForeignKey('User', related_name='received_messages')
    sent_time = models.DateTimeField(null=True, blank=True)
    message = models.CharField(max_length=3000, blank=True)
    received_deleted = models.IntegerField(null=True, blank=True)
    sent_deleted = models.IntegerField(null=True, blank=True)
    read_status = models.CharField(max_length=3, blank=True)

    class Meta:
        db_table = u'messages'


class ReadStatus(models.Model):
    user_id = models.ForeignKey('User', null=True, blank=True)
    article_id = models.ForeignKey('Article', null=True, blank=True)
    status = models.CharField(max_length=3, blank=True)

    class Meta:
        db_table = u'read_status'


class ReadStatusOrg(models.Model):
    user_id = models.ForeignKey('User', null=True, blank=True)
    board_id = models.ForeignKey('Board', null=True, blank=True)
    read_status_data = models.TextField(blank=True)
    read_status_numbers = models.TextField(blank=True)
    read_status_markers = models.TextField(blank=True)

    class Meta:
        db_table = u'read_status_org'


class ScrapStatus(models.Model):
    user_id = models.ForeignKey('User')
    article_id = models.ForeignKey('Article')

    class Meta:
        db_table = u'scrap_status'


class SelectedBoard(models.Model):
    user_id = models.ForeignKey('User', null=True, blank=True)
    board_id = models.ForeignKey('Board', null=True, blank=True)

    class Meta:
        db_table = u'selected_boards'


class UserActivation(models.Model):
    user_id = models.ForeignKey('User', primary_key=True)
    activation_code = models.CharField(max_length=150, unique=True, blank=True)
    issued_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = u'user_activation'


class User(models.Model):
    username = models.CharField(max_length=120, unique=True, blank=True)
    password = models.CharField(max_length=150, blank=True)
    nickname = models.CharField(max_length=120, blank=True)
    email = models.CharField(max_length=180, unique=True, blank=True)
    signature = models.CharField(max_length=3072, blank=True)
    self_introduction = models.CharField(max_length=3072, blank=True)
    default_language = models.CharField(max_length=15, blank=True)
    campus = models.CharField(max_length=45, blank=True)
    activated = models.IntegerField(null=True, blank=True)
    widget = models.IntegerField(null=True, blank=True)
    layout = models.IntegerField(null=True, blank=True)
    join_time = models.DateTimeField(null=True, blank=True)
    last_login_time = models.DateTimeField(null=True, blank=True)
    last_logout_time = models.DateTimeField(null=True, blank=True)
    last_login_ip = models.CharField(max_length=45, blank=True)
    is_sysop = models.IntegerField(null=True, blank=True)
    authentication_mode = models.IntegerField(null=True, blank=True)
    listing_mode = models.IntegerField(null=True, blank=True)
    activated_backup = models.IntegerField(null=True, blank=True)
    deleted = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = u'users'


class Visitor(models.Model):
    total = models.IntegerField(primary_key=True)
    today = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = u'visitors'


class Welcome(models.Model):
    content = models.TextField(blank=True)
    issued_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    valid = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = u'welcomes'

