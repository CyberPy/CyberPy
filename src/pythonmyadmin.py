# coding=utf-8

# pythonMyAdmin V1.0
# (c) 2023 CyberPy
# https://github.com/CyberPy
# License: MIT

from __future__ import unicode_literals
from builtins import str
from builtins import next
from builtins import range
from builtins import object
from sys import modules
C = modules['MAIN'].C
C.Module.module_access(
	__name__
	)

def usr_exists(id=None):
    sql = C.Snippet(
        'SELECT USER FROM ',
        User.db_name,
        ".USERS WHERE USER = '" )
    id = id or INFO.address('id')
    sql.join(escape_sql(id), "'")
    query = MySQLAPI.query(
        sql.element,
        fetch = True,
        dictcursor = False
        ) or []
    return bool(len(query))

class Interpreter(object):
	err = Errors()
	@staticmethod
	def isstr(obj):
		return isinstance(obj, str
		) or isinstance(obj, bytes)
	@staticmethod
	def code():
		raw = untext(INFO.address(
			'code')).replace(
			    b'\n', b'\n\t')
		return b'\n\t'.__add__(raw)
	@classmethod
	def script(cls):
		return b'def script():'.__add__(
		    cls.code()
		    ).__add__(b'\nC.Interpreter.func = script')
	@classmethod
	def alg(cls):
		txt = cls.script()
		exec(txt)
		return cls.func
	@classmethod
	def execute(cls):
		alg = cls.err.stats(cls.alg)
		err_case = IfElse(
			lambda: alg,
			lambda: cls.err.stats(alg)
			)
		return err_case.value(
			cls.isstr(alg)
			)
	@classmethod
	def evaluate(cls):
		exe = cls.execute()
		return str(exe)

class Console(object):
	err = Errors()
	@staticmethod
	def isfetch():
		return INFO.address(
			'console'
			) == 'fetch'
	@staticmethod
	def code():
		instr = INFO.address(
			'code'
			).split(';')
		pyg = PyGod()
		pyg.length = len(instr)
		pyg.index = 0
		end = lambda: pyg.index == pyg.length
		empty = lambda: instr[pyg.index] == ''
		def remove(self, items):
			items.pop(pyg.index)
			self.length -= 1
			self.index -= 1
		pop = lambda: remove(pyg, instr)
		exe = IfElse(
			pop,
			lambda: None
			)
		while not end():
			exe.action(empty())
			pyg.index += 1
			if end():
				break
		return instr
	@classmethod
	def execute(cls, instruction):
		return MySQLAPI.query(
			instruction,
			fetch=cls.isfetch()
			)
	@classmethod
	def encode(cls):
		code = cls.code()
		for i in range(len(code)):
			code[i] = cls.execute(
				code[i]
				)
		layer = lambda: len(code) == 1
		while layer():
			code = code[0]
			if not layer():
				break
		return str(code)
	@classmethod
	def sql(cls):
		snip = Snippet()
		enc = cls.encode
		add = lambda: snip.add(enc())
		cls.err.attempt(add)
		return snip.string()

class PMA_UI(object):
	img404 = C.Doc()
	img404.create_element(
		'div',
		'<h1 id="msg404">MySQL Error</h1>',
		style='text-align:center;width:85%')
	img404.image(
		'/pythonMyAdmin/images/404.pma.png',
		'404 Not Found'
		)
	img404[1].prop(UI.id, 'img404')
	img404.merge()

	nav = C.UI.create_element(
		'nav', '', id='pma_nav')

	footer = C.Doc()
	footer.create_element(
	    'a', '<< Home',
	    href="/")
	footer.append(UI.hr)
	footer.create_element(
	    'h3', 'POWERED BY')
	footer.create_element(
		'a',
		'CyberPy (Python Framework)',
		href='''https://
		github.com/
		CyberPy/
		CyberPy''',
		clss='credits',
		target='_blank')
	footer.create_element(
		'a',
		'ClassicQuery (JS Framework)',
		href='''https://
		github.com/
		CyberPy/
		ClassicQuery''',
		clss='credits',
		target='_blank')
	footer.append(
		u'<p>© CyberPy 2018</p>')
	footer.wrap('footer')

	head = C.Doc()
	head.create_element(
		'script',
		'',
		src='''/pythonMyAdmin
		/min/pma.og.js''')
	head.create_element(
		'link',
		rel='stylesheet',
		href='''/pythonMyAdmin
		/min/pma.og.css''')
	head.create_element(
		'title', 'pythonMyAdmin')
	head.append('''<meta name="viewport"
	content="width=device-width,
	initial-scale=1">''')
	head.wrap('head')

	form = C.Doc()
	form.create_element(
		'p', 'Username: ', id='usrinput')
	form.text_input('usr')
	form.append(UI.br)
	form.create_element(
		'p', 'Password: ', id='pwdinput')
	form.password_input('pwd')
	form.submit_input('Submit')
	form[-1].prop(UI.id, 'submitinput')
	form[-1].prop(UI.value, 'Login')
	form.wrap(
		'form',
		method='POST',
		action='/pythonmyadmin')

	csl_input = C.Doc()
	csl_input.textarea_input(**{
		'id': 'sqlbox',
		'innertext': '''
		-- Click "Execute" to execute sql//-
		-- Click "Fetch" to fetch data//-
		-- To import a database, upload a
	    SQL file & execute//-//-
		SHOW DATABASES''',
		' spellcheck="%s"': 'false'})
	csl_input.merge()

	csl_exec = UI.create_element(
		'button',
		'Execute',
		id='execsql',
		onclick='''session.
		pma.console.execSQL()''')
	csl_fetch = UI.create_element(
		'button',
		'Fetch',
		id='fetchsql',
		onclick='''session.
		pma.console.fetchSQL()''')
	csl_clear = UI.create_element(
		'button',
		'Clear',
		onclick='''session.
		pma.console.clear()''')
	csl_export = UI.create_element(
		'button',
		'Export',
		onclick='''session.
		pma.console.db.export()''')
	csl_upload = '''<input type="file"
		onchange="session.pma.
		console.script.getFile()"
		id="upload">'''

	csl_prog = '''<div id="progbox">
	<p id="progpercent">0%</p>
	<div id="progcontainer"><div id="progbar"></div></div>
	</div>'''

	interpreter = C.Doc()
	interpreter.textarea_input(**{
		'id':'scriptbox',
		'innertext':'''
		# click 'Execute' to execute
		//-//-return 'Hello World'
		''',
		' spellcheck="%s"': 'false'
		})
	interpreter.merge()

	sandbox_input = C.Doc()
	sandbox_input.textarea_input(
		**{
			'id': 'sandbox',
			' spellcheck="%s"': 'false',
			'innertext': '''
			// Click "Execute" to execute
			//-//-var cc = new CreditCard('1234123412341234');
			//-//-return cc.check();'''
			})
	sandbox_input.merge()

	sandbox_exec = UI.create_element(
		'button',
		'Execute',
		id='execsandbox',
		onclick='''session.
		pma.sandbox.execJS()''')
	sandbox_clear = UI.create_element(
		'button',
		'Clear',
		onclick='''session.
		pma.sandbox.clear()''')

	cms = C.Doc()
	cms.append('''
		<div id="cmsloadbox" class="loadicons">
			<div></div>
			<div></div>
			<div></div>
		</div>
		<select class="cmslist" id="cmstables"
		onchange="session.pma.cms.reset()">
			<option value="pages">Pages</option>
			<option value="users">Users</option>
		</select>
	''')
	cms.create_element(
		'button',
		'Launch',
		id='cmsgo',
		clss='cmsbtn',
		onclick='''session.
		pma.cms.getPages()''')
	cms.create_element(
		'button',
		'Reset',
		id='cmsreset',
		clss='cmsbtn',
		onclick='''session.
		pma.cms.reset()''')
	cms.create_element(
		'div', '',
		id='cmsbox')
	cms.merge()

	@classmethod
	def set_accordion(cls):
		acc = C.Accordion()
		acc.store_bookmarks(
			'Databases',
			'Tables',
			'Models',
			'Properties',
			'Value',
			'Console',
			'CMS',
			'Interpreter',
			'Sandbox'
			)
		acc.create(
			(('<p>databases</p>'),),
			(('''Select a Database
			 to show its Tables'''),),
			(('''Select a Table
			 to show its Models'''),),
			(('''Select a Model to
			 show its Properties'''),),
			(('''Select a Property
			 to show a Value'''),),
			(('''<div id="dbloadbox" class="loadicons">
			<div></div><div></div><div></div>
			</div><p>Enter SQL:
			</p><br>'''),
			(
				''.join([
					cls.csl_input.element,
					cls.csl_prog,
					UI.br, UI.br,
					cls.csl_exec,
					cls.csl_fetch,
					cls.csl_clear,
					cls.csl_export,
					UI.br, UI.br,
					cls.csl_upload,
					UI.br])
				),
			('''
			<div id='sqlres'>
				<p>- Running MySQL</p>
			</div>''')),
			((cls.cms.element),),
			(
				('CyberPy is installed.'),
				('To return a value, include a "return" statement.'),
				('<p>Enter Python:</p>'),
				(
					cls.interpreter.element
					),
				(
					'''<button
					 id="execbutton">
					Execute</button>
					<button
					 id="execclear">
					Clear</button>'''
					),
				(
					UI.box(
						'scriptresult',
						'<p>- Running Main.py</p>'
						)
					)
				),
			(
				('ClassicQuery is installed.'),
				('To return a value, include a "return" statement.'),
				(cls.sandbox_input.element),
				(cls.sandbox_exec),
				(cls.sandbox_clear),
				(
					UI.box(
						'sandboxres',
						'<p>- Running pma.js</p>'
						)
					)
				)
			)
		cls.accordion = acc.element.replace(
			'/image',
			'/pythonMyAdmin/images'
			).replace('.png', '.pma.png')
		cls.accordion = UI.create_element(
		    'a',
		    '<button class="logout">Logout</button>',
		    href="/pythonMyAdmin?logout=true",
		    ).__add__(cls.accordion)

	@classmethod
	def create_accordion(cls, databases):
		return cls.accordion.replace(
			'<p>databases</p>', databases
			).__add__('''<script>
			document.cookie="session=ok;";
			</script>''')

	@classmethod
	def template(cls, body):
		body.wrap('main')
		body.append(cls.nav)
		body.append(body.string())
		body.append(cls.footer.element)
		body.wrap('body')
		doc = C.Doc(
			cls.head.element,
			body.element)
		doc.wrap('html')
		return doc

PMA_UI.set_accordion()

class PythonMyAdmin(object):
	err = Errors()
	classes = Switch(
		**{
			'1': 'pma',
			'2': 'pma_db',
			'3': 'pma_tb',
			'4': 'pma_model',
			'5': 'pma_prop',
			'6': 'pma_prop'
			}
		)
	def __init__(self):
		if INFO.hasnext():
			next(INFO)
		self.request = Switch(
			**{
				'gapi': self.gapi,
				'query': self.query,
				'console': self.console,
				'evaluate': self.evaluate,
				'': self.embed
				}
			)
	def __image(self):
		FILE.downdir('images')
		FILE.getfile(
			INFO.liveaddress()
			)
		factory = ContentFactory()
		factory.content = FILE.bincontent()
		factory.contenttype(
			'image',
			'png'
			)
		factory.def_static_cache()
		factory.gzip()
		return factory
	def __text(self):
		FILE.downdir('min')
		FILE.getfile(
			INFO.liveaddress()
			)
		factory = ContentFactory()
		factory.setcontent(FILE.content())
		typ = C.Snippet(
			Substring.after(
				INFO.liveaddress(),
				'.'))
		typ.replaces(**{
			'min.': '',
			'og.': ''})
		factory.contenttype(
			'text', 'javascript' if typ.element == 'js' else typ.element)
		factory.def_static_cache()
		factory.min()
		factory.gzip()
		return factory
	def __html(self, html):
		factory = ContentFactory()
		factory.setcontent(html)
		factory.default(cache = False)
		return factory
	def evaluate(self):
		return Snippet(
			'- ',
			Interpreter.evaluate(),
			).string()
	def __action_btn(self, action, path):
		callback = Snippet(
			'session.pma.',
			action
			).element
		return UI.create_element(
			'button',
			'',
			**{
				'clss': Snippet(
					'pma_',
					action
					).element,
				' data-callback="%s"': callback,
				''' data-data='
				{"action":"%s"}' ''': action,
				' data-uri="%s"':
				Path.relpath(*path),
				' onclick="%s"':
				'session.pma.itemClick(this)',
				' title="%s"': action.title()
				}
			)
	def __create_btn(self, path):
		return self.__action_btn(
			'create',
			path[:len(path) - 1]
			)
	def __update_btn(self, path):
		return self.__action_btn(
			'update',
			path
			)
	def __read_btn(self, path):
		return self.__action_btn(
			'read',
			path
			)
	def __delete_btn(self, path):
		return self.__action_btn(
			'delete',
			path
			)
	def __classname(self, num):
		return self.classes.address(
			str(num)
			)
	def __uri_btn(self, path, title):
		resrc = path[len(path) - 1]
		if title:
			resrc = resrc.title()
		return UI.create_element(
			'strong',
			'<p>',
			resrc,
			'</p>',
			clss='pma_title'
			)
	def __uri_item(self, path, title, okdel=True):
		classname = self.__classname(
			len(path) - 1
			)
		btns = [
			self.__uri_btn(path, title),
			self.__read_btn(path),
			self.__update_btn(path)
			]
		delbtn = self.__delete_btn
		tobtns = btns.append
		exe = IfElse(
			lambda: tobtns(delbtn(path)),
			lambda: btns.pop(1)
			)
		exe.action(okdel)
		return UI.create_element(
			'li',
			*btns,
			clss=classname
			)
	def __list_title(self, path):
		return UI.tag(
			UI.h1,
			path[len(
				path
				) - 2].title()
			)
	def __uri_list(self, items, default=True, title=True):
		item_count = len(items)
		list_title = self.__list_title(
			items[0]
			)
		crbtn = self.__create_btn
		create = IfElse(
			lambda: crbtn(items[0]),
			lambda: ''
			)
		createval = create.value(default)
		for i in range(item_count):
			items[i] = self.__uri_item(
				items[i],
				title,
				okdel=default
				)
		item_box = UI.create_element(
			'ul',
			*items,
			clss='pma_repr'
			)
		return Snippet(
			list_title,
			createval,
			item_box
			).string()
	def __pathify(self, path, items):
		count = len(items)
		for i in range(count):
			item = [
				'pythonMyAdmin',
				'query'
				]
			item.extend(path)
			item.append(items[i])
			items[i] = item
		return items
	def __getpath(self):
		path = []
		INFO.key = 'query'
		while True:
			path.append(
				INFO.liveaddress()
				)
			if INFO.hasnext():
				next(INFO)
			else:
				break
		INFO.key = 'query'
		return path
	def get_databases(self):
		return self.__uri_list(
			self.__pathify(
				[],
				CRUD.read_db()
				)
			)
	def create_db(self):
		CRUD.create_db()
		return self.get_databases()
	def del_db(self):
		CRUD.del_db()
		return self.get_databases()
	def update_db(self):
		CRUD.update_db()
		return self.get_databases()
	def databases(self):
		crud = Switch(
			**{
				'create': self.create_db,
				'read': self.get_tables,
				'update': self.update_db,
				'delete': self.del_db
				}
			)
		return crud.value(
			INFO.address('action')
			)
	def create_tb(self):
		CRUD.create_tb()
		return self.get_tables()
	def get_tables(self):
		return self.__uri_list(
			self.__pathify(
				self.__getpath(),
				CRUD.read_tb()
				)
			)
	def update_tb(self):
		CRUD.update_tb()
		return self.get_tables()
	def del_tb(self):
		CRUD.del_tb()
		return self.get_tables()
	def tables(self):
		crud = Switch(
			**{
				'create': self.create_tb,
				'read': self.get_models,
				'update': self.update_tb,
				'delete': self.del_tb
				}
			)
		return crud.value(
			INFO.address('action')
			)
	def get_models(self):
		return self.__uri_list(
			self.__pathify(
				self.__getpath(),
				CRUD.read_model()
				)
			)
	def create_model(self):
		CRUD.create_model()
		return self.get_models()
	def update_model(self):
		CRUD.update_model()
		return self.get_models()
	def del_model(self):
		CRUD.del_model()
		return self.get_models()
	def models(self):
		crud = Switch(
			**{
				'create': self.create_model,
				'read': self.get_props,
				'update': self.update_model,
				'delete': self.del_model
				}
			)
		return crud.value(
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
		return crud.value(
			INFO.address('action')
			)
	def create_prop(self):
		CRUD.create_prop()
		return self.get_props()
	def update_prop(self):
		CRUD.update_prop()
		return self.get_props()
	def del_prop(self):
		CRUD.del_prop()
		return self.get_props()
	def get_props(self):
		return self.__uri_list(
			self.__pathify(
				self.__getpath(),
				CRUD.read_prop()
				)
			)
	def get_value(self):
		return self.__uri_list(
			self.__pathify(
				self.__getpath(),
				[CRUD.read_value()]
				),
			default=False,
			title=False
			)
	def update_value(self):
		CRUD.update_value()
		return self.get_value()
	def value(self):
		crud = Switch(
			**{
				'read': self.get_value,
				'update': self.update_value,
				}
			)
		return crud.value(
			INFO.address('action')
			)
	def __queries(self):
		return Switch(
			**{
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
	def query(self):
		queries = self.__queries()
		count = str(self.__querycount())
		query_flow = IfElse(
			lambda: queries.value(count),
			lambda: 'Query Error'
			)
		return query_flow.value(
			queries.has(count)
			)
	def pma(self):
		value = self.request.value(
			INFO.liveaddress()
			)
		return self.__html(value)
	def __dbrequest(self):
		is_api = INFO.has('api')
		pma_flow = IfElse(
			lambda: C.API().load(),
			self.pma
			)
		return pma_flow.value(is_api)
	def serve_request(self):
		pma_flow = IfElse(
			self.__dbrequest,
			self.signin
			)
		return pma_flow.value(
			CyberLog.isset() and User().auth()
			)
	def serve_file(self):
		FILE.setfile(C.__file__)
		is_image = INFO.liveaddress(
			) == 'images'
		next(INFO)
		pma_flow = IfElse(
			self.__image,
			self.__text
			)
		pma_file = pma_flow.value(
			is_image
			)
		FILE.reset()
		return pma_file
	def __isfile(self):
		current = INFO.address(
			'pythonmyadmin'
			)
		is_image = current == 'images'
		is_text = current == 'min'
		return is_text or is_image
	def load(self):
		pma_flow = IfElse(
			self.serve_file,
			self.serve_request
			)
		met = pma_flow.address(
			self.__isfile()
			)
		item = []
		alg = lambda: item.append(met())
		self.err.attempt(alg)
		INFO.empty()
		return item[0]
	def console(self):
		return Snippet(
			'- ',
			DataType.string(
				Console.sql()
				)
			).string()
	def gapi(self):
		googleUser = GoogleUser()
		return json.dumps(googleUser.__dict__)
	def template(self, body_html):
		body = C.Doc(body_html)
		doc = PMA_UI.template(body)
		return UI.doctype.__add__(doc.element)
	def signin(self):
		html = self.template(
			PMA_UI.form.element)
		return self.__html(html)
	def embed(self):
		try:
			res = PMA_UI.create_accordion(
				self.get_databases()
				)
		except:
			res = PMA_UI.img404.element
		return self.template(res)

API.custom['usr_exists'] = usr_exists
