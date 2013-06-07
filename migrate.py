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

    for source in targets.all():
        target = target_model()
        for f in fields:
            setattr(target, f, getattr(source, f))

        if fieldmap:
            for k, v in fieldmap.iteritems():
                setattr(target, v, getattr(source, k))

        if extra:
            extra(source, target)

        target.save(force_insert=True)

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

def main():
    # Step 1. Migrate Accounts
    accounts()

if __name__ == '__main__':
    main()
