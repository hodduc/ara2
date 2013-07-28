# -*- coding: utf-8 -*-
''' Custom Hasher for ara
기존 ara에서 사용하던 hash function을 호환하기 위해 필요한 Hash algorithm 구현체
'''

import crypt
import random
import string

from django.utils.crypto import constant_time_compare
from django.contrib.auth.hashers import BasePasswordHasher

class OldAraPasswordHasher(BasePasswordHasher):
    SALT_SET = string.lowercase + string.uppercase + string.digits + './'
    algorithm = "arara-old"

    def salt(self):
        return ''.join(random.sample(self.SALT_SET, 2))

    def _crypt(self, password, salt):
        pw = crypt.crypt(password, salt)
        asc1 = pw[1:2]
        asc2 = pw[3:4]

        i = 96 # ord('0') + ord('0')
        try:
            i = ord(asc1) + ord(asc2)
        except TypeError:
            pass

        while True:
            pw = crypt.crypt(pw, pw)
            i += 1
            if not (i % 13 != 0):
                break

        return pw

    def verify(self, password, encoded):
        password = password.strip()
        algorithm, iterations, _, hash = encoded.split('$', 3)
        password_2 = self._crypt(password, hash)
        return constant_time_compare(password_2, hash)

    def encode(self, raw_password, salt):
        return "%s$1$$%s" % (self.algorithm, self._crypt(raw_password, salt))

    def safe_summary(self, encoded):
        return {'password': encoded, 'algorithm': self.algorithm}
