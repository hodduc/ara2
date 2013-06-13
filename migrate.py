#! /usr/bin/env python
#-*- coding: utf-8 -*-
'''
Database Migration Script for ara2 project
This script migrate DB for arara(based on SQLAlchemy 0.6) to ara2's django ORM.

usage:
    First, clear ara main db, and execute syncdb to create tables.
    Then, execute "python migrate.py".
'''

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ara2.settings")
import sys

def direct_migrate(source_model, target_model, fields, fieldmap=None, extra=None, filter_func=None):
    '''
    주어진 source model을 그대로 target_model로 복사
    source_model: Django Model
    target_model: Django Model
    fields: Tuple of field name. (필드 이름이 양쪽에서 같은 경우)
    fieldmap: Dict of fields (source 필드이름 => target 필드이름)
    extra: extra work function. sourceobj, targetobj 를 받는 함수형 객체여야 함
    filter_func: filtering function. queryset을 받아 queryset을 리턴해야 함.
    '''

    targets = source_model.objects.using('oldara')
    targets = filter_func(targets) if filter_func else targets

    def chunk_queryset(qs):
        counter = 0
        chunk_size = 1000
        count = qs.count()
        while counter < count:
            print >>sys.stderr, 'chunk %d' % counter
            for model in qs[counter:counter+chunk_size]:
                yield model
            counter += chunk_size

    for source in chunk_queryset(targets.all()):
        target = target_model()
        for f in fields:
            setattr(target, f, getattr(source, f))

        if fieldmap:
            for k, v in fieldmap.iteritems():
                setattr(target, v, getattr(source, k))

        if extra:
            extra(source, target)

        target.save(force_insert=True)

def copy_table(source_db, source_table, target_db, target_table, fields, fieldmap=None):
    '''
    주어진 table을 ORM을 거치지 않고 SQL을 통해 그대로 복사
    단 HOST가 같아야 하고, target 쪽 USER에게 양 DB 접근 권한이 모두 있어야 함

    source_db: settings.DATABASES 중 source
    source_table: source table name
    target_db: settings.DATABASES 중 target
    target_table: target table name
    fields: Tuple of field name. (필드 이름이 양쪽에서 같은 경우): DB에 저장되는 raw 필드명
    fieldmap: Dict of fields (source 필드이름 => target 필드이름)
    '''

    assert source_db['HOST'] == target_db['HOST']

    select_fields, insert_fields = zip(*fieldmap.iteritems()) if fieldmap else [], []
    select_fields += fields
    insert_fields += fields

    assert len(select_fields) == len(insert_fields)

    import _mysql
    db = _mysql.connect(host=(target_db['HOST'] or 'localhost'),
                        user=target_db['USER'],
                        passwd=target_db['PASSWORD'])
    db.query("""SET FOREIGN_KEY_CHECKS = 0;""")
    db.query("""DELETE FROM %s.%s;""" % (target_db['NAME'], target_table))
    db.query("""INSERT INTO %s.%s (%s) SELECT %s FROM %s.%s;""" %
            (target_db['NAME'], target_table, ','.join(insert_fields),
                ','.join(select_fields), source_db['NAME'], source_table))
    db.query("""SET FOREIGN_KEY_CHECKS = 1;""")

    db.close()

def accounts():
    '''
    Account/models.py에 대한 마이그레이션을 진행함

    1. 기존 스키마에서 layout, widget은 아라라에서 사용하고 있지 않으므로 삭제함
    2. join_time, activated, is_sysop, last_login_time은 비슷한 이름의 model field가 User에
       존재하므로 해당 필드를 이용하는 것으로 수정함
    3. authentication_mode는 왠지 모르겠으나 값이 0 아니면 NULL만 들어 있으므로,
       일단 2(KAIST 메일인증)으로 수정
    4. username의 길이가 기존 40자에서 30자로 줄어듬. 이 영향을 받는 회원이 2013년 6월 기준
       2명 존재하나 둘 다 실제로 사용하는 계정은 아님.
    '''

    # Migrate User.
    from ara2.account.models import User
    from oldara.models import User as OldUser

    def user_extra(source, target):
        # password migration. Add algorithm prefix.
        target.password = 'arara-old$1$$' + source.password.strip()

        # possible default_language: eng, en, kor, ko_KR, ko, nor
        if source.default_language in ('kor', 'ko', 'ko_KR'):
            target.default_language = 'ko'
        else:
            target.default_language = 'en'

        # possible campus: Daejeon, Seoul, '' (empty)
        if source.campus.lower() == 'seoul':
            target.campus = 'seoul'
        else:
            target.campus = 'daejeon'

        # possible authentication_mode: 0, NULL
        target.authentication_mode = 2

        # HACK for email. email SHOULD NOT be NULL
        if source.email is None:
            target.email = "noexist@ara.kaist.ac.kr"

        # Truncate username
        if len(source.username) > 30:
            target.username = source.username[:30]

        # Give superuser flag to sysop
        if target.is_staff:
            target.is_superuser = True

    direct_migrate(OldUser, User,
                ('id', 'username', 'password', 'nickname', 'email',
                    'signature', 'self_introduction', 'last_logout_time',
                    'last_login_ip', 'is_sysop', 'listing_mode', 'activated_backup', 'deleted'),
                {'activated': 'is_active', 'is_sysop': 'is_staff', 'join_time': 'date_joined'},
                extra=user_extra)

                # XXX last_login_time

    user_list = OldUser.objects.values('id').all()

    # Migrate LostPasswordToken. Depends on User.
    from ara2.account.models import LostPasswordToken
    from oldara.models import LostPasswordToken as OldLostPasswordToken
    direct_migrate(OldLostPasswordToken, LostPasswordToken,
                ('id', 'user_id', 'code'))

    # Migrate UserActivation. Depends on User.
    from ara2.account.models import UserActivation
    from oldara.models import UserActivation as OldUserActivation

    direct_migrate(OldUserActivation, UserActivation,
                ('user_id', 'activation_code', 'issued_date'),
                filter_func=lambda queryset: queryset.filter(user_id__in=user_list))

    # Migrate Message. Depends on User.
    from ara2.account.models import Message
    from oldara.models import Message as OldMessage

    def message_extra(source, target):
        if source.from_ip is None:
            target.from_ip = ''

    direct_migrate(OldMessage, Message,
                ('id', 'from_user_id', 'from_ip', 'to_user_id', 'sent_time', 'message',
                    'received_deleted', 'sent_deleted', 'read_status'),
                extra=message_extra)

def misc():
    '''
    main/models.py와 기타 모델에 대한 마이그레이션을 진행함
    '''

    from oldara.models import Banner as OldBanner
    from ara2.main.models import Banner

    direct_migrate(OldBanner, Banner,
            ('id', 'content', 'issued_date', 'due_date', 'valid', 'weight'))

    from oldara.models import Visitor as OldVisitor
    from ara2.main.models import Visitor

    direct_migrate(OldVisitor, Visitor,
            ('total', 'today', 'date'))

def boards():
    '''
    board/models.py에 대한 마이그레이션을 진행함
    '''

    from oldara.models import Category as OldCategory
    from ara2.board.models import Category

    direct_migrate(OldCategory, Category,
            ('id', 'category_name', 'order'))

    from oldara.models import Board as OldBoard
    from ara2.board.models import Board

    direct_migrate(OldBoard, Board,
            ('id', 'category_id', 'board_name', 'board_alias', 'board_description',
                'deleted', 'read_only', 'hide', 'order', 'type', 'to_read_level',
                'to_write_level'))

    from oldara.models import BoardHeading as OldBoardHeading
    from ara2.board.models import BoardHeading

    direct_migrate(OldBoardHeading, BoardHeading,
            ('id', 'board_id', 'heading'))


    # Article과 Vote는 테이블이 너무 크기 때문에, MySQL 쿼리로 직접 옮긴다
    from ara2.settings import DATABASES
    from oldara.models import Article as OldArticle
    from ara2.board.models import Article

    copy_table(DATABASES['oldara'], OldArticle._meta.db_table,
                DATABASES['default'], Article._meta.db_table,
                ('id', 'title', 'content', 'date', 'board_id', 'heading_id',
                    'author_id', 'author_nickname', 'author_ip', 'hit',
                    'positive_vote', 'negative_vote', 'deleted', 'destroyed',
                    'is_searchable', 'root_id', 'parent_id', 'reply_count',
                    'last_modified_date', 'last_reply_date', 'last_reply_id'))

#    direct_migrate(OldArticle, Article,
#            ('id', 'title', 'content', 'date', 'board_id', 'heading_id',
#                'author_id', 'author_nickname', 'author_ip', 'hit',
#                'positive_vote', 'negative_vote', 'deleted', 'destroyed',
#                'is_searchable', 'root_id', 'parent_id', 'reply_count',
#                'last_modified_date', 'last_reply_date', 'last_reply_id'))

    from oldara.models import ArticleVoteStatus as OldVote
    from ara2.board.models import ArticleVoteStatus as Vote

    copy_table(DATABASES['oldara'], OldVote._meta.db_table,
                DATABASES['default'], Vote._meta.db_table,
                ('id', 'article_id', 'user_id'))

#    direct_migrate(OldVote, Vote,
#            ('id', 'article_id', 'user_id'))

    from oldara.models import BbsManager as OldManager
    from ara2.board.models import BbsManager

    direct_migrate(OldManager, BbsManager,
            ('id', 'board_id', 'manager_id'))

    from oldara.models import Blacklist as OldBlacklist
    from ara2.board.models import Blacklist

    direct_migrate(OldBlacklist, Blacklist,
            ('id', 'user_id', 'blacklisted_user_id', 'blacklisted_date',
                'last_modified_date', 'block_article', 'block_message'))

    from oldara.models import BoardNotice as OldNotice
    from ara2.board.models import BoardNotice

    direct_migrate(OldNotice, BoardNotice,
            ('article_id', ))

    from oldara.models import File as OldFile
    from ara2.board.models import File

    direct_migrate(OldFile, File,
            ('id', 'filename', 'saved_filename', 'filepath',
                'user_id', 'board_id', 'article_id', 'deleted'))

    from oldara.models import ScrapStatus as OldScrap
    from ara2.board.models import ScrapStatus

    direct_migrate(OldScrap, ScrapStatus,
            ('id', 'user_id', 'article_id'))

    from oldara.models import SelectedBoard as OldSelectedBoard
    from ara2.board.models import SelectedBoard

    direct_migrate(OldSelectedBoard, SelectedBoard,
            ('id', 'user_id', 'board_id'))

def main():
    # Step 1. Migrate Accounts
    accounts()

    # Step 2. Migrate misc
    misc()

    # Step 3. Migrate boards & articles
    boards()

if __name__ == '__main__':
    main()
