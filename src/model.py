# coding=utf-8

from __future__ import print_function
from __future__ import unicode_literals
from builtins import next
from builtins import str
from builtins import range
from builtins import object
from sys import modules
C = modules['MAIN'].C
C.Module.module_access(
	__name__
	)

class MySQLAPI(object):
	def __init__(
		self,
		dbname):
		super(
			MySQLAPI,
			self).__init__()
		self.dbname = Censor.filter(dbname).upper()
		self.db = self.dbconnect(self.dbname)
		self.cursor = self.db.cursor(
			MySQLdb.cursors.DictCursor
			)
	@classmethod
	def database(cls, dbname):
		db = cls.connect()
		db.cursor().execute(
			Snippet(
				'CREATE DATABASE ',
				'IF NOT EXISTS ',
				dbname.upper(),
				' CHARACTER SET utf8 ',
				'COLLATE utf8_general_ci;'
				).string()
			)
		db.close()
	@classmethod
	def checkdb(cls, dbname):
		db = cls.connect()
		cursor = db.cursor()
		sql = Snippet(
			"SHOW DATABASES LIKE '",
			dbname.upper(),
			"'"
			).string()
		tup = cursor.execute(sql)
		db.close()
		return tup > 0
	@classmethod
	def checktb(cls, dbname, tbname):
		db = cls.dbconnect(dbname.upper())
		cursor = db.cursor()
		sql = Snippet(
			"SHOW TABLES LIKE '",
			tbname.upper(),
			"'"
			).string()
		tup = cursor.execute(sql)
		db.close()
		return tup > 0
	@classmethod
	def dropdb(cls, dbname):
		db = cls.connect()
		db.cursor().execute(
			Snippet(
				'DROP DATABASE ',
				dbname.upper()
				).string()
			)
		db.close()
	@staticmethod
	def connect():
		return MySQLdb.connect(
			host=HOSTNAME,
			port=PORTNUMBER,
			user=USERNAME,
			passwd=PASSWORD)
	@classmethod
	def query(
		cls,
		sql,
		fetch=False,
		dictcursor=True):
		db = cls.connect()
		if dictcursor:
			cursor = db.cursor(
				MySQLdb.cursors.DictCursor
				)
		else:
			cursor = db.cursor()
		try:
			cursor.execute(sql)
			if fetch:
				result = list(
					cursor.fetchall()
					)
			else:
				result = 'Success'
			db.commit()
			db.close()
			return result
		except Exception:
			db.rollback()
			db.close()
			Errors.log()
			return 'Failed'
	@staticmethod
	def __sqllist(cursor):
		sqllist = []
		sqllist.extend(
			cursor.fetchall()
			)
		for i in range(len(sqllist)):
			sqllist[i] = sqllist[i][0]
		return sqllist
	@classmethod
	def dblist(cls):
		db = cls.connect()
		cursor = db.cursor()
		cursor.execute(
			'SHOW DATABASES'
			)
		dbs = cls.__sqllist(cursor)
		db.close()
		return dbs
	@staticmethod
	def dbconnect(dbname):
		return MySQLdb.connect(
			host=HOSTNAME,
			port=PORTNUMBER,
			user=USERNAME,
			passwd=PASSWORD,
			db=dbname.upper(),
			charset='utf8')
	@classmethod
	def setindex(cls, dbname, tbname):
		db = cls.dbconnect(dbname.upper())
		cursor = db.cursor()
		index = tbname[
			:len(tbname) - 1
			]
		sql = Snippet(
				'CREATE INDEX ',
				'tbindex ON ',
				tbname.upper(),
				' (',
				index,
				')'
				).string()
		cursor.execute(sql)
		db.close()
	def primary(self, tbname):
		sql = Snippet(
			'SHOW KEYS FROM ',
			tbname.upper(),
			" WHERE Key_name = 'PRIMARY'"
			).string()
		self.cursor.execute(sql)
		result = self.cursor.fetchall()
		self.db.close()
		return result[0]['Column_name']
	@classmethod
	def check_mysql(cls):
		try:
			cls.connect().close()
			return True
		except MySQLdb.Error:
			return False
	@classmethod
	def tblist(cls, dbname):
		db = cls.dbconnect(dbname.upper())
		cursor = db.cursor()
		cursor.execute(
			'SHOW TABLES'
			)
		tbs = cls.__sqllist(cursor)
		db.close()
		return tbs
	def __sortdata(
		self,
		dict):
		datalist = []
		for key in dict:
		    item = (
				key,
				dict[key].replace("'", "''")
				)
		    datalist.append(item)
		param = Snippet()
		arg = Snippet()
		last_data_item = datalist[len(datalist) - 1]
		for key in datalist:
			param.add(key[0])
			param.add(
				Delimiter.comma(
					key, last_data_item
					)
				)
			arg.insert("'%s'", key[1])
			arg.add(
				Delimiter.comma(
					key, last_data_item
					)
				)
		return (param.element, arg.element)
	def create(
		self,
		tbname,
		data):
		table = Snippet(
			'CREATE TABLE IF NOT EXISTS '
			)
		table.insert("%s ", tbname.upper())
		table.insert("(%s)", data)
		return table.element
	def checktable(self, tbname):
		check = Snippet(
			'SHOW TABLES LIKE '
			)
		check.insert("'%s'", tbname.upper())
		return check.element
	def cleartable(self, tbname):
		clear = Snippet(
			'TRUNCATE TABLE '
			)
		check.insert('%s', tbname.upper())
		return self.do(check.element)
	def insert(
		self,
		tbname,
		data):
		datalist = self.__sortdata(data)
		params = Snippet()
		params.insert('(%s) ', datalist[0])
		args = Snippet()
		args.insert('VALUES (%s)', datalist[1])
		sql = Snippet()
		sql.add('INSERT INTO ')
		sql.add(tbname.upper())
		sql.add(params.element)
		sql.add(args.element)
		return sql.element
	def update(
		self,
		tbname,
		data):
		sql = Snippet(
			'UPDATE ',
			tbname.upper(),
			' SET ',
			data['slot']
			)
		sql.insert(
			" = '%s'",
			data['new']
			)
		sql.join(
			' WHERE ',
			data['condition']
			)
		sql.insert(
			" = '%s'",
			data[
				'status'
				].replace("'", "''")
			)
		return sql.string()
	def delete(
		self,
		tbname,
		data):
		sql = Snippet(
			'DELETE FROM ',
			tbname.upper(),
			' WHERE ',
			data['condition'],
			)
		sql.insert(
			" = '%s'",
			data[
				'status'
				].replace("'", "''")
			)
		return sql.string()
	def drop(self, tbname):
		sql = Snippet(
			'DROP TABLE IF EXISTS ',
			tbname.upper()
			).string()
		return sql
	def read(
		self,
		data,
		tbname):
		sql = Snippet(
			'SELECT ', data,
			' FROM ', tbname.upper()
			).string()
		all = []
		try:
			self.cursor.execute(sql)
			all.extend(
				self.cursor.fetchall()
				)
		except Exception:
			print(sql)
			Errors.log()
		self.db.close()
		return all
	def exp(self, func, col, tbname):
		sql = Snippet(
			'SELECT ', func.upper(),
			'(', col.upper(), ') FROM ',
			tbname.upper()).string()
		res = []
		try:
			self.cursor.execute(sql)
			res.extend(
				self.cursor.fetchall()
				)
			for item in res[0]:
				res.append(res[0][item])
			res = res.pop()
		except Exception:
			res = ''
			print(sql)
			Errors.log()
		self.db.close()
		return res
	def do(self, sql):
		error = False
		try:
			self.cursor.execute(sql)
			self.db.commit()
		except Exception:
			error = True
			self.db.rollback()
			print(sql)
			Errors.log()
		self.db.close()
		return error

class ModelAPI(object):
    def __init__(
		self,
		dbname,
		tbname):
        super(
			ModelAPI,
			self
			).__init__()
        self.db = MySQLAPI(escape_sql(dbname, encode=False))
        self.object = escape_sql(
            Censor.filter(tbname))
    def create(self, props):
        self.db.do(
			self.db.create(
				self.object,
				props
				)
			)
    def update(
		self,
		data):
        # DATA is dict
        sql = self.db.update(
			self.object,
			data)
        self.db.do(sql)
    def get(
		self,
		anchor,
		stat):
        where = Snippet(
			self.object,
			' WHERE ')
        where.insert(
			'%s = ',
			escape_sql(anchor.upper()))
        where.insert(
			"'%s'",
			escape_sql(stat))
        return self.db.read(
			'*',
			where.element)
    def __checkpending(self, fetch):
        duplicate = lambda: 'duplicate'
        is_pending = fetch[0][3] == 'pending'
        condition = IfElse(
			self.is_new,
			duplicate)
        return condition.value(is_pending)
    def checkduplicate(
		self,
		anchorStat):
        fetch = self.get(anchorStat)
        has_fetched = len(fetch) > 0
        self.is_new = lambda: 'isnew'
        condition = IfElse(
			lambda: self.__checkpending(fetch),
			self.is_new
			)
        return condition.value(has_fetched)
    def add(self, data):
        # DATA is dict
		# keys must be all-caps
        self.db.do(
			self.db.insert(
				self.object,
				data
				)
			)
    def getall(self):
        return self.db.read(
			'*',
			self.object)
    def getone(
		self,
		anchor,
		stat):
        fetch = self.get(anchor, stat)
        has_fetched = len(fetch) > 0
        getfirst = lambda: fetch[0]
        error = lambda: 'Not Found'
        condition = IfElse(getfirst, error)
        res = condition.value(has_fetched)
        return res
    def delete(
		self,
		data):
        self.db.do(
			self.db.delete(
				self.object,
				data
				)
			)

class Model(object):
    def __init__(self, info=False):
        super(Model, self).__init__()
        if info:
            self.info()
        self.props = OrderedDict()
        self.indexkey = 'tbindex'
    def check_same(self, user):
        if user.auth():
            return True
        if not user.props:
            return None
        if not user.props['USER'
        ] == self.props['USER']:
            return None

        if C.SESSION.has_cybertoken():
            user.pw_valid = True

        valid = user.pw_valid
        if not valid:
            valid = self.props['PW'
            ] == user.props['PW']

        valid = valid and self.private_auth()
        if valid and self.has_auth():
            C.SESSION.add_user(self)
        return valid
    def check_public(self, usr_type):
        pub = usr_type == 'public'
        read = INFO.address('action') == 'read'
        return pub and read
    def check_user_type(self, user):
        usr_type = self.props['USERTYPE']
        if usr_type == 'private':
            return self.check_same(user)
        elif self.check_public(usr_type):
            return True
        else:
            return user.auth()
    def validate(self):
        Errors().attempt(self.populate)
        if not self.props:
            return False
        user = C.User()
        if 'USERTYPE' in self.props:
            return self.check_user_type(user)
        else:
            return user.auth()
    @staticmethod
    def has_auth():
        has_usr = INFO.has('usr')
        has_pwd = INFO.has('pwd')
        return has_pwd and has_usr
    def private_auth(self):
        if not self.has_auth():
            return True
        else:
            return C.Password().check(
                C.INFO.address('pwd'),
                C.decode_uri(self.props['PW']) )
    def info(self):
        INFO.key = 'query'
        self.db_name = C.INFO.liveaddress(
			).upper()
        next(INFO)
        self.tb_name = C.INFO.liveaddress(
			).upper()
    def set_indexval(self):
        lowtb = self.tb_name.lower()
        default = lambda: 'default_column'
        val = lambda: INFO.address(lowtb)
        hastb = INFO.has(lowtb)
        condition = IfElse(val, default)
        self.indexval = condition.value(
			hastb
			).title()
    def cols(self):
        sql = Snippet(
			'DESCRIBE ',
			self.db_name,
			'.',
			self.tb_name
			).string()
        return MySQLAPI.query(
			sql,
			fetch=True
			)
    def null(self):
        cols = self.cols()
        for col in cols:
            key = col['Field']
            self.props[key] = 'NULL'
    def unicode_props(self):
        for key in self.props:
            self.props[key] = text(self.props[key])
    def encode_props(self):
        for key in self.props:
            self.props[key] = C.encode_uri(
				self.props[key])
    def mysql_escape_props(self):
        for key in self.props:
            val = escape_sql(self.props[key])
            self.props[key] = val
    def decode_props(self):
        for key in self.props:
            self.props[key] = C.decode_uri(
				self.props[key])
    def data(self, key, value):
        self.props[key] = Censor.filter(value)
    def impdata(self, **kwargs):
        for key in kwargs:
            self.data(key, kwargs[key])
    def primcolumn(self):
        return MySQLAPI(
			self.db_name
			).primary(
				self.tb_name
				)
    def set_primcolumn(self):
        self.indexkey = self.primcolumn()
    def __log_create(self):
        C.LOG.log(
			Snippet(
				self.db_name,
				'.create( ',
				self.tb_name,
				' )'
				).string()
			)
    def create(self, log=True):
        # creates table
        api = ModelAPI(
			self.db_name,
			self.tb_name
			)
        datalist = []
        for key in self.props:
            item = (
				key,
				self.props[key])
            datalist.append(item)
        primary = Snippet(
			'PRIMARY KEY(',
			self.tb_name[
				:len(self.tb_name) - 1
				],
			')'
			).string()
        datalist.append((primary, ''))
        data_str = Snippet()
        last_item = datalist[
			len(datalist) - 1
			][0]
        for i in range(len(datalist)):
            data_str.add(
				Snippet(
					datalist[i][0],
					' ',
					datalist[i][1],
					Delimiter.comma(
						datalist[i][0],
						last_item
						)
					).string()
				)
        api.create(
			data_str.string()
			)
        MySQLAPI.setindex(
			self.db_name,
			self.tb_name
			)
        if log:
            self.__log_create()
    def __log_destroy(self):
        C.LOG.log(
			Snippet(
				self.db_name,
				'.',
				self.tb_name,
				'.destroy()'
				).string()
			)
    def destroy(self, log=True):
        # drops table
        api = MySQLAPI(self.db_name)
        api.drop(
			Censor.filter(
				self.tb_name
				)
			)
        if log:
            self.__log_destroy()
    def __log_add(self):
        C.LOG.log(
			Snippet(
				self.db_name,
				'.',
				self.tb_name,
				'.',
				self.indexkey,
				'.add(',
				self.indexval,
				')'
				).string()
			)
    def __add(self):
        api = ModelAPI(
			self.db_name,
			self.tb_name)
        self.mysql_escape_props()
        api.add(self.props)
    def add(
		self,
		log=True,
		useprimary=True):
        if useprimary:
            self.set_primcolumn()
        self.__add()
        if log:
            self.__log_add()
    def __log_delete(self):
        C.LOG.log(
			Snippet(
				self.db_name,
				'.',
				self.tb_name,
				'.',
				self.indexkey,
				'( ',
				self.indexval,
				' )',
				'.delete()'
				).string()
			)
    def __delete(self):
        data = {
			'condition': escape_sql(
				Censor.filter(self.indexkey)),
			'status': escape_sql(
			    Censor.filter(self.indexval))
			}
        api = ModelAPI(
			self.db_name,
			self.tb_name)
        api.delete(data)
    def delete(
		self,
		log=True,
		useprimary=True):
        if useprimary:
            self.set_primcolumn()
        self.__delete()
        if log:
            self.__log_delete()
    def __log_update(self, slot, newdata):
        C.LOG.log(
			Snippet(
				self.db_name,
				'.',
				self.tb_name,
				'.',
				self.indexkey,
				'(',
				self.indexval,
				').update( ',
				slot,
				', ',
				newdata,
				' )'
				).string()
			)
    def __update(self, slot, newdata):
        data = {
			'slot': escape_sql(
			    Censor.filter(slot)),
			'new': escape_sql(
			    Censor.filter(newdata)),
			'condition': escape_sql(
				Censor.filter(self.indexkey)),
			'status': escape_sql(
			    Censor.filter(self.indexval.title()))
			}
        api = ModelAPI(
			self.db_name,
			self.tb_name)
        api.update(data)
    def update(
		self,
		slot,
		newdata,
		log=True,
		useprimary=True):
        if useprimary:
            self.set_primcolumn()
        self.__update(slot, newdata)
        if log:
            self.__log_update(
				slot,
				newdata
				)
    def updateid(self, newdata, log=True):
        self.set_primcolumn()
        self.__update(self.indexkey, newdata)
        if log:
            self.__log_update(
				self.indexkey,
				newdata
				)
    def list_all(self):
        api = ModelAPI(
			self.db_name,
			self.tb_name)
        all = api.getall()
        C.LOG.log(
			Snippet(
				self.db_name,
				'.',
				self.tb_name,
				'.list_all()'
				).string()
			)
        return all
    def filter(self):
        api = ModelAPI(
			self.db_name,
			self.tb_name)
        objectlist = api.get(
			Censor.filter(self.indexkey),
			Censor.filter(self.indexval))
        return objectlist
    def __log_populate(self):
        C.LOG.log(
			Snippet(
				self.db_name,
				'.',
				self.tb_name,
				'.',
				self.indexkey,
				'(',
				self.indexval,
				').populate()'
				).string()
			)
    def __populate(self):
        api = ModelAPI(
			self.db_name,
			self.tb_name)
        self.props.update(
			api.getone(
				Censor.filter(
					self.indexkey
					),
				Censor.filter(
					self.indexval.upper()
					)
				)
			)
    def populate(
		self,
		log=True,
		useprimary=True):
        if useprimary:
            self.set_primcolumn()
        self.__populate()
        if log:
            self.__log_populate()
    def unload(self):
        for key in self.props:
            setattr(
				self,
				key.lower(),
				self.props[key])
        self.props.clear()
    def objectify(self, itemtuple):
        objectlist = []
        for item in itemtuple:
            for key in item:
                lower_key = key.lower()
                val = item[key]
                del item[key]
                item[lower_key] = val
            pyg = PyGod()
            pyg.import_dict(item)
            objectlist.append(pyg)
        return objectlist
    def all_objects(self):
        return self.objectify(
			self.list_all()
			)
    def modellize(self, items):
        model_type = type(self)
        model_list = []
        for item in items:
            model = type(
				model_type.__name__,
				(model_type,),
				item)
            model_list.append(model)
        return model_list
    def all_models(self):
        return self.modellize(
			self.list_all()
			)
    def exp(self, func, prop):
        api = MySQLAPI(self.db_name)
        return api.exp(
			func, prop,
			self.tb_name)
    def max(self, prop):
        return self.exp('MAX', prop)
    def min(self, prop):
        return self.exp('MIN', prop)
    def count(self):
        return self.exp('COUNT', self.indexkey)
    def avg(self, prop):
        return self.exp('AVG', prop)
    def sum(self, prop):
        return self.exp('SUM', prop)