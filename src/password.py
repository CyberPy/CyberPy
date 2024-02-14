# coding=utf-8

from __future__ import unicode_literals
from builtins import str
from builtins import object
from sys import modules
C = modules['MAIN'].C
C.Module.module_access(
	__name__
	)

class Password(object):
    def __init__(self):
        super(Password, self).__init__()
        self.valid = False
    def validate(self, key, val, pwd):
        try:
            user = USER_CLASS()
            user.view(key, val)
            self.valid = self.check(
				pwd,
				user.props['PASSWORD']
				)
        except:
            Errors.log()
    def encrypt(self, pwd):
        hash_salt = Snippet(
			self.salt(),
			'$',
			self.hash(pwd))
        return hash_salt.element
    def hash(self, arg):
        hash = hashlib.new('sha512')
        hash.update(str(arg).encode('utf-8'))
        return hash.hexdigest()
    def salt(self):
        return self.hash(urandom(16))
    def token(self, max):
        return self.hash(C.randint(0, max))
    def check(self, raw, db_hash):
        if '$' in db_hash:
            db_hash = db_hash.split('$')[1]
        return db_hash == self.hash(raw)