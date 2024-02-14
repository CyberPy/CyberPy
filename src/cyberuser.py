# coding=utf-8

from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
from builtins import range
from builtins import object
from sys import modules
C = modules['MAIN'].C
C.Module.module_access(
	__name__
	)

class TransferError(RuntimeError):
    def __init__(self):
        super(TransferError, self).__init__()

class SyncError(TransferError):
    def __init__(self):
        super(TransferError, self).__init__()

class MetaError(TransferError):
    def __init__(self):
        super(TransferError, self).__init__()

class CyberModel(Model):
	db_name = 'CYBERPY'

class Log(CyberModel):
    def __init__(self, log_id):
        super(
			Log,
			self
			).__init__()
        log = Snippet(
			log_id,
			'_logs'
			).string()
        self.tb_name = log.upper()
        self.indexkey = log[
			:len(log) - 1
			].upper()
        self.indexval = ''
    def refresh(self):
        timestamp = TimeStamp()
        stp = timestamp.current_datesec
        self.indexval = stp().title()
    def setaction(self, action, time):
        self.data(
			'LOG_ACTION',
			action
			)
        self.data(
			self.indexkey,
			time
			)
    def liveaction(self, action):
        self.refresh()
        self.setaction(
			action,
			self.indexval
			)
    def log(self, action, force_log=False):
        if force_log or C.LOG_ENABLED:
            self.liveaction(action)
            self.add(log=False)

class CyberLog(Log):
	def __init__(self):
		C.LOG = self
		if not MySQLAPI.checkdb(
			self.db_name
			):
			MySQLAPI.database(
				self.db_name
				)
		super(CyberLog, self
			).__init__('cyberpy')
		self.setaction(
			'VARCHAR(100)',
			'VARCHAR(100)'
			)
		if not MySQLAPI.checktb(
			self.db_name,
			self.tb_name
			):
			self.create()
		self.log(
			'__init__()',
			force_log=True)
	@staticmethod
	def isset():
		return 'LOG' in C.__dict__

class CMS(CyberModel):
	def __init__(self):
		super(CMS, self).__init__()
	def clear(self):
		MySQLAPI(self.db_name
		   ).cleartable(self.tb_name)
	def tb_exists(self):
		return MySQLAPI.checktb(
			self.db_name,
			self.tb_name)
	@classmethod
	def create_tables(cls):
		if MySQLAPI.checkdb(cls.db_name):
			Page().create_table()
			User().create_table()
			Session().create_table()

class Session(CMS):
	max = 1000
	counter = C.Counter(
		'seconds',
		expire=3600)
	def __init__(self, cookie='', **kwargs):
		super(Session, self).__init__()
		self.tb_name = 'SESSIONS'
		self.indexkey = 'SESSION'
		self.pwd = C.Password()
		self.err = C.Errors()
		self.cookies = []
		self.cookie = Cookie(cookie)
		if kwargs:
			self.cookie.load(kwargs)
	def has_cybertoken(self):
		return 'cybertoken' in self.cookie
	def set(self):
		if self.has_cybertoken():
			self.indexval = self.cookie[
				'cybertoken'].value
			self.add_cookie()
		for mor in list(self.cookie.values()):
			snip = C.Snippet(
				mor.key, '=',
				mor.value,
				';')
			self.cookies.append((
				'Set-Cookie',
				snip.element))
	def token(self):
		return self.pwd.token(self.max)
	def token_exists(self):
		self.indexval = self.token()
		return self.err.attempt(
			self.populate
			)
	def check_session(self):
		self.indexval = self.cookie[
			'cybertoken'].value
		INFO.ifcase('logout', 'false')
		if INFO.address('logout') == 'true':
			C.SESSION.reset()
			return None
		exists = self.err.attempt(self.populate)
		if exists:
			exists = self.refresh()
		return exists
	def calibrate(self):
		if self.counter.auto():
			MySQLAPI.cleartable(self.tb_name)
		else:
			self.max *= 2
	def unique_token(self):
		if self.max < self.count():
			self.calibrate()
		while self.token_exists():
			self.props.clear()
	def expired(self):
		now = int(C.time())
		start = int(self.props['TIME'])
		delay = now - start
		return C.USER_EXPIRES < delay
	def reset(self):
		if 'cybertoken' not in self.cookie:
			return
		C.SESSION.indexval = self.cookie[
		    'cybertoken'].value
		C.SESSION.delete()
		C.SESSION.props.clear()
		C.SESSION.cookie = Cookie()
		del C.SESSION.cookies[:]
	def end(self):
		try:
			self.reset()
			return 'success'
		except:
			return 'failed'
	def refresh(self):
		exp = self.expired()
		if exp:
			self.reset()
		return not exp
	def create_cookie(self):
		snip = C.Snippet(
		    'cybertoken=',
			self.indexval, '; Max-Age=',
			str(C.USER_EXPIRES), '; SameSite=',
			C.SAME_SITE, '; HttpOnly;')
		return snip.element
	def add_cookie(self):
		self.cookies.append(
		    ('Set-Cookie', self.create_cookie())
		    )
	def add_user(self, user):
		self.unique_token()
		self.impdata(
			SESSION = self.indexval,
			USER = user.props['USER'],
			USERTYPE = user.props['USERTYPE'],
			TIME = str(int(C.time())))
		self.add()
		self.add_cookie()
	def add_template(self):
		self.impdata(
			SESSION = 'CHAR(128)',
			USER = 'VARCHAR(25)',
			USERTYPE = 'VARCHAR(7)',
			TIME = 'CHAR(10)')
	def add_props(self):
		self.indexval = self.token()
		self.impdata(
			SESSION = self.indexval,
			USER = 'admin',
			USERTYPE = 'admin',
			TIME = str(int(C.time())))
	def create_table(self):
		if not self.tb_exists():
			self.add_template()
			self.create()
			self.add_props()
			self.add()

class AuthError(Exception):
	def __init__(self):
		super(AuthError, self).__init__(
			'Error: Authentication Failed')

class InfoError(AttributeError):
    def __init__(self):
        super(InfoError, self).__init__(
            'Error: Invalid or missing C.INFO.key'
            )

def check_infokey(key='web'):
    if INFO.has(INFO.address(key)):
        raise InfoError

class Page(CMS):
	def __init__(self):
		super(Page, self).__init__()
		self.tb_name = 'PAGES'
		self.indexkey = 'PAGE'
	def embed(self):
		C.LIVE_URL = Path.home_url(
		    *INFO.tolist('web'))
		if C.LIVE_URL.endswith('//'):
		    C.LIVE_URL = C.LIVE_URL[:-1]
		self.indexval = C.LIVE_URL
		if not self.validate():
			raise AuthError
		self.decode_props()
		C.TITLE = self.props['TITLE']
		C.DESCR = self.props['DESCRIPTION']
		C.Head.img = self.props['IMG']
		C.ROBOTS = self.props['ROBOTS']
		alt = self.props['ALT']
		if alt.endswith('}'
		) and alt.startswith('{'):
		    C.Href_Lang.urls.update(
			    C.json.loads(
			        self.props['ALT']
			        )
			    )
		return self.props['CONTENT']
	def add_template(self):
		self.impdata(
			PAGE = 'VARCHAR(80)',
			TITLE = 'VARCHAR(60)',
			DESCRIPTION = 'VARCHAR(160)',
			CONTENT = 'MEDIUMTEXT',
			ALT = 'TEXT',
			LANG = 'CHAR(2)',
			ROBOTS = 'VARCHAR(20)',
			IMG = 'VARCHAR(140)',
			USERTYPE = 'VARCHAR(7)')
	def add_props(self):
		self.impdata(
			PAGE = C.DOMAIN,
			TITLE = 'Home',
			DESCRIPTION = 'Default Homepage',
			CONTENT = u'Hello World :)',
			ALT = u'{}',
			LANG = 'en',
			ROBOTS = 'index,follow',
			IMG = '/image/logo.png',
			USERTYPE = 'public')
	def create_table(self):
		if not self.tb_exists():
			self.add_template()
			self.create()
			self.add_props()
			self.indexval = C.DOMAIN
			self.add()

class User(CMS):
	def __init__(self):
		super(User, self).__init__()
		self.tb_name = 'USERS'
		self.indexkey = 'USER'
		self.pwd = C.Password()
		self.err = C.Errors()
	def import_user(self):
		self.err.attempt(self.import_session)
		if 'USER'  in self.props:
			self.indexval = self.props['USER']
			self.props.clear()
			self.populate()
		elif self.has_auth():
			self.indexval = C.INFO.address('usr')
			self.err.attempt(self.populate)
	def import_session(self):
		C.SESSION.check_session()
		self.props.update(C.SESSION.props)
	def token_user(self):
		self.props.clear()
		self.import_session()
	def check_token_type(self):
		self.token_user()
		if not self.props:
			return False
		self.pw_valid = self.props[
			'USERTYPE'] == 'admin'
		return self.pw_valid
	def auth_user(self):
		self.props.clear()
		self.indexval = INFO.address('usr')
		self.err.attempt(self.populate)
	def check_auth_pwd(self):
		if C.SESSION.has_cybertoken():
			C.SESSION.reset()
		self.auth_user()
		self.pw_valid = self.check_pwd()
		if self.pw_valid:
			C.SESSION.add_user(self)
		return self.pw_valid
	def check_pwd(self):
		if not self.props:
			return None
		self.pw_valid = self.pwd.check(
			INFO.address('pwd'),
			decode_uri(self.props['PW']))
		is_admin = self.props[
			'USERTYPE'] == 'admin'
		return self.pw_valid and is_admin
	def auth(self):
		# check if admin
		valid = False
		if self.has_auth():
			valid = self.check_auth_pwd()
		elif C.SESSION.has_cybertoken():
			valid = self.check_token_type()
		return valid
	def add_template(self):
		self.impdata(
			USER = 'VARCHAR(25)',
			PW = 'TEXT',
			USERTYPE = 'VARCHAR(7)')
		self.create()
	def add_admin(self):
		self.props.clear()
		self.impdata(
			USER = 'admin',
			PW = self.pwd.encrypt('admin'),
			USERTYPE = 'admin')
		self.indexval = 'admin'
		self.add()
	def add_public(self):
		self.props.clear()
		self.impdata(
			USER = 'public',
			PW = self.pwd.encrypt('public'),
			USERTYPE = 'public')
		self.indexval = 'public'
		self.add()
	def create_table(self):
		if not self.tb_exists():
			self.add_template()
			self.add_admin()
			self.add_public()


class Connection(object):
	def __init__(self):
		self.dblist = C.MySQLAPI.dblist()
	def finddb(self):
		for db in self.dblist:
			if CyberModel.db_name in db.upper():
				CyberModel.db_name = db
	def set(self):
		self.finddb()
		C.LOG = CyberLog()
		CMS.create_tables()

if MySQLAPI.check_mysql():
	Connection().set()

def get_user():
    if not C.USER:
        C.USER = User()
        C.USER.import_user()
    return C.USER

def ok_session():
    user = get_user()
    return str(bool(user.props)).lower()

def ok_admin():
    auth = User().auth()
    return str(bool(auth)).lower()

C.API.custom.update({
    'ok_session': ok_session,
    'ok_admin': ok_admin
    })

if 'crypt' in globals():
	class GoogleUser(PyGod):
		def __init__(self, gsuite_domain=False):
			self.no_idtoken = KeyError('idtoken missing')
			self.invalid = crypt.AppIdentityError(
				'invalid user'
				)
			self.domain_error = crypt.AppIdentityError(
				'wrong domain'
				)
			self.gsuite_domain = gsuite_domain
			self.validate()
		def info(self):
			clientinfo = client.verify_id_token(
				INFO.address('idtoken'),
				CLIENTID
				)
			idinfo = {}
			for key in clientinfo:
				idinfo[str(key)] = clientinfo[key]
			return idinfo
		def is_valid(self, idinfo):
			accounts = [
				'accounts.google.com',
				'https://accounts.google.com'
				]
			return idinfo['iss'] in accounts
		def validate(self):
			try:
				if not INFO.has('idtoken'):
					raise self.no_idtoken
				idinfo = self.info()
				if not self.is_valid(idinfo):
					raise self.invalid
				if self.bad_domain(idinfo):
					raise self.domain_error
				self.__dict__.clear()
				self.import_dict(idinfo)
			except (
				KeyError,
				crypt.AppIdentityError
				) as noauth:
				print(noauth)
		@staticmethod
		def __same_dom(idinfo):
			if 'hd' in idinfo:
				dom = Snippet(DOMAIN)
				dom.filters('http://', 'https://')
				return idinfo['hd'] == dom.string()
		def bad_domain(self, idinfo):
			if self.gsuite_domain:
				return self.__same_dom(idinfo)