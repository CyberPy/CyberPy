# coding=utf-8

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

class CRUD(object):
	err = Errors()
	@classmethod
	def read(cls, src):
		data = []
		action = data.extend
		alg = lambda: action(src())
		cls.err.attempt(alg)
		return data
	@classmethod
	def create_db(cls):
		if not C.User().auth():
			return None
		new = INFO.address(
			'new'
			).upper()
		action = MySQLAPI.database
		alg = lambda: action(new)
		cls.err.attempt(alg)
		cls.__createdef_tb(new)
	@classmethod
	def __createdef_tb(cls, dbname):
		INFO.key = 'query'
		INFO.setval(dbname)
		INFO.nextval('default_models')
		cls.create_tb()
	@classmethod
	def read_db(cls):
		return MySQLAPI.dblist()
	@staticmethod
	def __copy_tbl_alg(base):
		item = lambda tbl: [base, '.', tbl]
		join = lambda itm: ''.join(itm)
		alg = lambda tbl, itm: join(itm(tbl))
		return lambda tbl: alg(tbl, item)
	@classmethod
	def __copy_old_tbl_alg(cls):
		return cls.__copy_tbl_alg(
			C.INFO.address(
				'pythonmyadmin'
				)
			)
	@classmethod
	def __copy_new_tbl_alg(cls):
		return cls.__copy_tbl_alg(
			C.INFO.address('new')
			)
	@classmethod
	def __copy_tbl_commands(cls):
		tbl = PyGod()
		tbl.old = cls.__copy_old_tbl_alg()
		tbl.new = cls.__copy_new_tbl_alg()
		return tbl
	@classmethod
	def __tables(cls):
		tables = cls.read_tb()
		commands = cls.__copy_tbl_commands()
		for i in range(len(tables)):
			tbl = PyGod()
			tbl.old = table.old(
				tables[i]
				)
			tbl.new = table.new(
				tables[i]
				)
			tables[i] = tbl
		return tables
	@staticmethod
	def __copytbl_sql(tbl):
		return Snippet(
			'INSERT INTO ',
			tbl.old,
			' SELECT * from ',
			tbl.new,
			''
			).string()
	@classmethod
	def __copytbl_queries(cls):
		tables = cls.__tables()
		for i in range(len(tables)):
			tables[i] = cls.__copytbl_sql(
				tables[i]
				)
		return tables
	@classmethod
	def __copy_db(cls):
		queries = cls.__copytbl_queries()
		connection = MySQLAPI.connect()
		cursor = connection.cursor()
		for query in queries:
			cursor.execute(
				query
				)
		connection.close()
	@classmethod
	def update_db(cls):
		if not C.User().auth():
			return None
		dbname = INFO.address(
			'query').lower()
		cls.create_db()
		cls.err.attempt(
			cls.__copy_db
			)
		INFO.delthis()
		cls.del_db(db_name=dbname)
	@classmethod
	def del_db(cls, db_name=None):
		if not C.User().auth():
			return None
		if not db_name:
			db_name = INFO.liveaddress().lower()
		action = MySQLAPI.dropdb
		alg = lambda: action(db_name)
		cls.err.attempt(alg)
	@staticmethod
	def __tbinfo():
		INFO.key = 'query'
		if not INFO.hasnext():
			INFO.nextval(
				INFO.address('new')
				)
			return INFO.key
	@classmethod
	def create_tb(cls):
		if not C.User().auth():
			return None
		is_tb = cls.__tbinfo()
		model = cls.__info_model()
		primary = model.tb_name[
			:len(model.tb_name) - 1
			]
		model.data(primary, 'VARCHAR(100)')
		cls.err.attempt(
			model.create
			)
		model.data(primary, 'Default Value')
		cls.err.attempt(
			model.add
			)
		if is_tb:
			INFO.delcase(is_tb)
	@classmethod
	def read_tb(cls):
		db_name = INFO.liveaddress(
			).upper()
		tblist = MySQLAPI.tblist
		alg = lambda: tblist(db_name)
		return cls.read(alg)
	@staticmethod
	def rename_tb():
		if not C.User().auth():
			return None
		next(INFO)
		return Snippet(
			'RENAME TABLE ',
			INFO.liveaddress(),
			' TO ',
			INFO.address(
				'new'
				).upper()
			).string()
	@classmethod
	def update_tb(cls):
		if not C.User().auth():
			return None
		INFO.key = 'query'
		mysql = MySQLAPI(
			INFO.liveaddress()
			)
		mysql.do(cls.rename_tb())
		INFO.delthis()
	@staticmethod
	def del_tb():
		if not C.User().auth():
			return None
		INFO.key = 'query'
		mysql = MySQLAPI(
			INFO.liveaddress()
			)
		next(INFO)
		sql = mysql.drop(
			INFO.liveaddress()
			)
		mysql.do(sql)
		INFO.delthis()
	@staticmethod
	def __info_model():
		return Model(info=True)
	@classmethod
	def create_model(cls):
		model = cls.__info_model()
		model.null()
		if 'USERTYPE' in model.props:
		    model.data('USERTYPE', 'private')
		model.set_primcolumn()
		model.data(
			model.indexkey,
			INFO.address('new')
			)
		cls.err.attempt(
			model.add
			)
	@classmethod
	def __def_model(cls):
		model = cls.__info_model()
		model.set_indexval()
		if not model.validate():
			return None
		if 'PW' in model.props:
		    if model.props['USERTYPE'] != 'admin': del model.props['PW']
		return model
	@staticmethod
	def __primaries(model, models):
		prims = []
		for item in models:
			prim = item[model.indexkey]
			prims.append(str(prim))
		return prims
	@classmethod
	def read_model(cls):
		if not C.User().auth():
			return None
		model = cls.__info_model()
		model.set_primcolumn()
		models = []
		ext = models.extend
		lst = model.list_all
		all = lambda: ext(lst())
		cls.err.attempt(all)
		prim = cls.__primaries
		alg = lambda: prim(model, models)
		prims = []
		cls.err.attempt(
			lambda: prims.extend(alg())
			)
		return prims
	@classmethod
	def update_model(cls):
		model = cls.__info_model()
		model.set_primcolumn()
		next(INFO)
		model.indexval = INFO.liveaddress()
		if not model.validate():
			return None
		upd = model.updateid
		new = INFO.address('new')
		alg = lambda: upd(new)
		cls.err.attempt(alg)
		INFO.delthis()
	@classmethod
	def del_model(cls):
		model = cls.__info_model()
		model.set_primcolumn()
		next(INFO)
		model.indexval = INFO.liveaddress()
		if not model.validate():
			return None
		model.delete()
		INFO.delthis()
	@staticmethod
	def __column():
		return INFO.address(
			'new'
			).split(',')
	@classmethod
	def __valid_prop(cls):
		props = cls.read_prop()
		col = cls.__column()
		# col == ['col_name',
		# 'col_type', 'val']
		is3 = len(col) == 3
		is_valid = col not in props
		return is_valid and is3
	@classmethod
	def create_prop(cls):
		if cls.__valid_prop():
			col = cls.__column()
			col[0] = col[0].upper()
			model = cls.__def_model()
			mysql = MySQLAPI(
				model.db_name
				)
			sql = Snippet(
				'ALTER TABLE ',
				model.tb_name,
				' ADD ',
				col[0],
				' ',
				col[1]
				).string()
			alg = lambda: mysql.do(sql)
			cls.err.attempt(alg)
			upd = model.update
			alg = lambda: upd(col[0], col[2])
			cls.err.attempt(alg)
	@classmethod
	def read_prop(cls):
		model = cls.__def_model()
		return list(model.props.keys())
	@classmethod
	def read_props(cls):
		return [#'*',
		*cls.read_prop()]
	@staticmethod
	def datatype(tb_name, col):
		sql = Snippet(
			'SELECT COLUMN_TYPE ',
			'FROM INFORMATION_',
			'SCHEMA.COLUMNS ',
			"WHERE table_name = '",
			tb_name,
			"' AND COLUMN_NAME = '",
			col.upper(),
			"'"
			).string()
		return MySQLAPI.query(
			sql,
			fetch=True,
			dictcursor=False
			)[0][0]
	@classmethod
	def update_prop(cls):
		if not C.User().auth():
			return None
		if cls.__check_prop():
			key = INFO.key
			prop = INFO.liveaddress()
			model = cls.__info_model()
			datatype = cls.datatype(
				model.tb_name,
				prop.upper()
				)
			mysql = MySQLAPI(
				model.db_name
				)
			sql = Snippet(
				'ALTER TABLE ',
				model.tb_name,
				' CHANGE COLUMN ',
				prop.upper(),
				' ',
				INFO.address(
					'new'
					).upper(),
				' ',
				datatype
				).string()
			alg = lambda: mysql.do(sql)
			cls.err.attempt(alg)
			INFO.delcase(key)
	@classmethod
	def __check_prop(cls):
		props = cls.read_prop()
		INFO.move(2)
		col = INFO.liveaddress()
		return col.upper() in props
	@classmethod
	def del_prop(cls):
		if not C.User().auth():
			return None
		if cls.__check_prop():
			key = INFO.key
			prop = INFO.liveaddress()
			model = cls.__info_model()
			mysql = MySQLAPI(
				model.db_name
				)
			sql = Snippet(
				'ALTER TABLE ',
				model.tb_name,
				' DROP COLUMN ',
				prop.upper()
				).string()
			alg = lambda: mysql.do(sql)
			cls.err.attempt(alg)
			INFO.delcase(key)
	@classmethod
	def load_model(cls):
		model = cls.__def_model()
		INFO.move(2)
		return model
	@classmethod
	def read_value(cls):
		model = cls.load_model()
		prop = INFO.liveaddress().upper()
		if prop == '*':
		    return model.props
		val = model.props[prop]
		return str(val)
	@classmethod
	def __update_val(cls):
		model = cls.load_model()
		if not model:
			return None
		key = INFO.liveaddress()
		val = INFO.address('new')
		user_type = key.upper() == 'USERTYPE'
		admin = C.User().auth()
		if user_type and not admin:
		    return None
		INFO.case('old', str(
			model.props[key.upper()])
			)
		model.update(key, text(val))
	@classmethod
	def update_value(cls):
		cls.err.attempt(
			cls.__update_val
			)
		next(INFO)
		INFO.delthis()

class Format(object):
	@staticmethod
	def href(target):
		pathlist = INFO.tolist('mode')
		pathlist.append(target)
		return Path.relpath(*pathlist)
	@staticmethod
	def link(href, rel, method):
		return {
			'href': href,
			'rel': rel,
			'method': method
			}
	@classmethod
	def get(cls, href, rel):
		return cls.link(
			href,
			rel,
			'GET'
			)
	@classmethod
	def getlist(cls, href):
		return cls.get(
			href,
			'list'
			)
	@classmethod
	def getself(cls, href):
		return cls.get(
			href,
			'self'
			)
	@classmethod
	def post(cls, href):
		return cls.link(
			href,
			'create',
			'POST'
			)
	@classmethod
	def put(cls, href):
		return cls.link(
			href,
			'edit',
			'PUT'
			)
	@classmethod
	def delete(cls, href):
		return cls.link(
			href,
			'delete',
			'DELETE'
			)
	@classmethod
	def edit(cls, href):
		return [
			cls.post(href),
			cls.put(href),
			cls.delete(href)
			]
	@classmethod
	def urilist(cls, href, index, item):
		links = [cls.getlist(href)]
		if item != '*': links.extend(cls.edit(href))
		return cls.packuri(index, item, links)
	@classmethod
	def packuri(cls, id, new, links):
		return {
			'id': id,
			'new': new,
			'links': links
			}
	@classmethod
	def pack(cls, uris):
		return {INFO.last('api'): uris}
	@classmethod
	def tolist(cls, list_method):
		uris = []
		index = 0
		for item in list_method():
			href = cls.href(item)
			uris.append(
				cls.urilist(href, index, item)
				)
			index += 1
		return cls.pack(uris)
	@classmethod
	def dblist(cls):
		return cls.tolist(CRUD.read_db)
	@classmethod
	def tblist(cls):
		return cls.tolist(CRUD.read_tb)
	@classmethod
	def modellist(cls):
		return cls.tolist(CRUD.read_model)
	@classmethod
	def proplist(cls):
		return cls.tolist(CRUD.read_props)
	@classmethod
	def value(cls, item=None):
		if not item:
			item = {'query': CRUD.read_value()}
		if isinstance(item, dict):
			return item
		href = cls.href(item)
		if INFO.has('old'):
			href = href.replace(
				INFO.address('old'),
				INFO.address('new'),
				1)
		uri = [cls.put(href)]
		return cls.pack(
			cls.packuri(0, item, uri)
			)

class API(object):
	err = Errors()
	custom = {
	    'logout': lambda: C.SESSION.end()
	    }
	def __init__(self):
		self.response = {}
		self.version = '1.0'
		self.custom = dict(self.custom)
		self.custom.update({
		    'bundle': self.loads
		    })
	def create_db(self):
		CRUD.create_db()
		return self.get_databases()
	def get_databases(self):
		dblist = Format.dblist()
		self.response['version'] = self.version
		self.response.update(dblist)
	def update_db(self):
		CRUD.update_db()
		return self.get_databases()
	def del_db(self):
		CRUD.del_db()
		return self.get_databases()
	def create_tb(self):
		CRUD.create_tb()
		return self.get_tables()
	def get_tables(self):
		self.response.update(
			Format.tblist()
			)
	def update_tb(self):
		CRUD.update_tb()
		return self.get_tables()
	def del_tb(self):
		CRUD.del_tb()
		return self.get_tables()
	def create_model(self):
		CRUD.create_model()
		return self.get_models()
	def get_models(self):
		self.response.update(
			Format.modellist()
			)
	def update_model(self):
		CRUD.update_model()
		return self.get_models()
	def del_model(self):
		CRUD.del_model()
		return self.get_models()
	def create_prop(self):
		CRUD.create_prop()
		return self.get_props()
	def get_props(self):
		self.response.update(
			Format.proplist()
			)
	def update_prop(self):
		CRUD.update_prop()
		return self.get_props()
	def del_prop(self):
		CRUD.del_prop()
		return self.get_props()
	def get_value(self):
		self.response.update(
			Format.value()
			)
	def update_value(self):
		CRUD.update_value()
		self.response.update(
			Format.value(
				item=INFO.address('new')
				))
	def databases(self):
		crud = Switch(
			**{
				'create': self.create_db,
				'read': self.get_tables,
				'update': self.update_db,
				'delete': self.del_db
				}
			)
		crud.action(
			INFO.address('action')
			)
	def tables(self):
		crud = Switch(
			**{
				'create': self.create_tb,
				'read': self.get_models,
				'update': self.update_tb,
				'delete': self.del_tb
				}
			)
		crud.action(
			INFO.address('action')
			)
	def models(self):
		crud = Switch(
			**{
				'create': self.create_model,
				'read': self.get_props,
				'update': self.update_model,
				'delete': self.del_model
				}
			)
		crud.action(
			INFO.address('action')
			)
	def props(self):
		crud = Switch(
			**{
				'create': self.create_prop,
				'read': self.value,
				'update': self.update_prop,
				'delete': self.del_prop
				}
			)
		crud.action(
			INFO.address('action')
			)
	def value(self):
		crud = Switch(
			**{
				'read': self.get_value,
				'update': self.update_value,
				}
			)

		crud.action(
			INFO.address('action')
			)
	def __queries(self):
		return Switch(
			**{
				'-1': self.get_databases,
				'0': self.databases,
				'1': self.tables,
				'2': self.models,
				'3': self.props,
				'4': self.value
				}
			)
	def __querycount(self):
		INFO.key = 'query'
		length = len(
			INFO.tolist('query')
			)
		if INFO.address(
			'action'
			) != 'create':
			length -= 1
		return length
	def notfound(self):
		self.response = 404
	def query(self):
		queries = self.__queries()
		count = str(self.__querycount())
		query_flow = IfElse(
			lambda: queries.action(count),
			lambda: self.notfound
			)
		query_flow.action(
			queries.has(count)
			)
	def json_resp(self):
		factory = ContentFactory()
		factory.setcontent(
			json.dumps(self.response)
			)
		factory.contenttype(
			'application',
			'json'
			)
		factory.gzip()
		return factory
	def embed(self):
		api = C.INFO.address('api')
		if api in self.custom:
			self.response = {
				'query': self.custom[api]()
				}
		else:
			self.err.attempt(self.query)
	def check(self):
		found = self.response != 404
		noerr = self.response != {}
		return found and noerr
	def load(self):
		self.embed()
		if not self.check():
			self.response = {'query': 'error'}
		return self.json_resp()
	def loads(self):
		try:
			reqs = json.loads(C.INFO.address('REQS'))
		except:
			self.response = {'query': 'error'}
			return self.json_resp()

		resps = []
		for req in reqs:
			C.INFO.case(
			    self.__class__.__name__.lower(),
			    req['uri'] )
			C.INFO.case(
			    'action',
			    C.WSGI.crud.address(req['method'])
			    )
			if req['user_cache'] != '1':
				C.USER = None
			C.INFO.options.update(req['data'])
			try:
				api = self.__class__()
				api.embed()
				resps.append( api.response['query'] )
			except:
				resps.append('error')

		return resps

def set_api(api=API):
    C.API_CLASS = api
    C.MODES.ifcase('api', C.API_CLASS)