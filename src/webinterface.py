# coding=utf-8

from __future__ import print_function
from __future__ import unicode_literals
from future import standard_library
standard_library.install_aliases()
from builtins import next
from builtins import str
from builtins import range
from builtins import object
from sys import modules
C = modules['MAIN'].C
C.Module.module_access(
	__name__
	)

class HTTP(Snippet):
	def __init__(self, *args):
		super(
			HTTP,
			self
			).__init__(*args)
		self.check_cert = True
	def simple_request(self, func, url, *args):
		self.status = func(
			url,
			headers={
				'content-type': 'text/plain',
				'user-agent': DOMAIN
				},
			auth=args,
			verify=self.check_cert
			)
		self.setval(self.status.text)
	def get(self, url, *args):
		self.simple_request(
			requests.get,
			url,
			*args
			)
	def delete(self, url, *args):
		self.simple_request(
			requests.delete,
			url,
			*args
			)
	def data_request(
		self,
		func,
		url,
		*args,
		**kwargs):
		self.status = func(
			url,
			data=kwargs,
			headers={
				'content-type': 'text/plain',
				'user-agent': DOMAIN
				},
			auth=args,
			verify=self.check_cert
			)
		self.setval(self.status.text)
	def post(self, url, *args, **kwargs):
		self.data_request(
			requests.post,
			url,
			*args
			**kwargs
			)
	def put(self, url, *args, **kwargs):
		self.data_request(
			requests.put,
			url,
			*args,
			**kwargs
			)

class Body(object):
    def __init__(self):
        super(
			Body,
			self
			).__init__()
    def __setlang(self, delete):
        C.INFO.case(
			'LANG',
			C.INFO.address('web')
			)
        lang = lambda: C.INFO.address('LANG')
        setweb = lambda web: C.INFO.case('web', web)
        keylang = lambda: C.INFO.has(lang())
        condition = IfElse(
			lambda: setweb(
				C.INFO.address(lang())
				),
			lambda: setweb(''))
        if delete:
            condition.action(keylang())
        if delete and keylang():
            C.INFO.delcase(lang())
    def __checklang(self, delete):
        web_length = len(
			C.INFO.address('web')
			)
        if web_length == 2:
            self.__setlang(delete)
    def set_payload_lang(self, delete=False):
        self.__checklang(delete)
    def main(self):
        web = C.WEBS.value(
			C.INFO.liveaddress())
        return web.embed()
    def page(self):
        main = Page().embed()
        try:
            main = C.decode_uri(main)
            main = C.decode_uri(main)
        except:
            pass
        try:
            main = main.replace("\\'", "'")
        except:
            pass
        return main
    def embed(self):
        error = Exception(
			'Error in <main></main>'
			)
        try:
            if C.WEBS.has(C.INFO.liveaddress()):
                main = self.main()
            else:
                main = self.page()
            if main == None:
                raise error
            return UI.tag(UI.main, main)
        except Exception:
            print(error)
    def load_nav(self):
        error = Exception(
			'Error in NAV_CLASS'
			)
        try:
            nav = C.NAV_CLASS().load()
            if nav == None:
                raise error
            return nav
        except Exception:
            print(error)
    def load(self):
        error = Exception(
			'Error in Nav and/or Main'
			)
        try:
            main = self.embed()
            return UI.tag(
		        self.load_nav(),
			    main
			    )
        except Exception:
            print(error)

class Web(object):
    credit = '''<!--//-//-
	POWERED BY://-//-
	CyberPy//-
	(c) 2016-2018//-
	https://github.com/CyberPy//-
	License: MIT//-//--->'''
    def __init__(self):
        super(Web, self).__init__()
        next(C.INFO)
        self.embed = C.INFO.address(
			'embed') == 'true'
    def getbody(self):
        error = Exception(
			'Error in BODY_CLASS'
			)
        try:
            bodyclass = C.BODY_CLASS()
            condition = IfElse(
		        bodyclass.embed,
			    bodyclass.load
			    )
            load = condition.address(
			self.embed
			)
            body = load()
            if body == None:
                raise error
            return UI.tag(
			    UI.body,
			    body
			    )
        except Exception:
            print(error)
    def gethead(self):
        error = Exception(
			'Error in META_CLASS'
			)
        try:
            meta = C.META_CLASS.load()
            if meta == None:
                raise error
            return meta
        except Exception:
            print(error)
    def setlang(self):
        C.LANG.case(
			'og',
			C.LANG.address('og').replace(
				C.DEF_LANG,
				C.INFO.address('LANG')
				)
			)
        C.LANG.case(
			'html',
			C.LANG.address('html').replace(
				C.DEF_LANG,
				C.INFO.address('LANG')
				)
			)
    def createdoc(self):
        error = Exception(
			'Error in head and/or body'
			)
        try:
            body = self.getbody()
            self.setlang()
            head = self.gethead()
            no_body = body == None
            no_head = head == None
            no_val = no_body or no_head
            if no_val:
                raise error
            return Snippet(
	            UI.doctype,
		        UI.create_element(
			        'html',
					self.credit,
				    head,
				    body,
				    lang=C.LANG.address('html'),
				    prefix='og: http://ogp.me/ns#')
			    ).string()
        except Exception:
            print(error)
    def load(self):
        docfail = Exception(
			'Document Failure'
			)
        try:
            doc = self.createdoc()
            if doc == None:
                raise docfail
            content_factory = ContentFactory()
            content_factory.lastmod(WSGI.def_cache)
            content_factory.headers.append(
				(
					'Content-Language',
					str(C.LANG.address('html')))
				)
            content_factory.setcontent(doc)
            read = C.INFO.address('action') == 'read'
            C.INFO.ifcase('cache', True)
            cache = C.INFO.address('cache')
            content_factory.default(
                cache = C.CACHE and read and cache
                )
            return content_factory
        except Exception:
            print(docfail)

class Redirect(object):
	urls = Switch()
	@classmethod
	def add(cls, old, new):
		cls.urls.case(
			Path.home_url(*old),
			Path.fullpath(*new)
			)
	@classmethod
	def has(cls, url):
		return cls.urls.has(url)
	@classmethod
	def forward(cls, url):
		return cls.urls.address(url)

C.INFO = CursorSwitch()
C.ACTIONS.extend(
	[
		C.INFO.empty,
		C.INFO.reset_default,
		Head.reset
		]
	)

def uaddress(key):
	return text(C.INFO.address(key))

def uliveaddress():
	return text(C.INFO.liveaddress())

class URLError(ValueError):
	def __init__(self):
		super(
			URLError, self
			).__init__(
				''.join([
					'URLError: ',
					C.LIVE_URL,
					' is not loopable'
					]))

class WSGI(object):
	cache_isset = False
	crud = Switch(
		**{
			'POST': 'create',
			'GET': 'read',
			'PUT': 'update',
			'DELETE': 'delete'
			}
		)
	def __init__(
		self,
		environ,
		start_response):
		super(WSGI, self).__init__()
		if not self.cache_isset:
			self.set_cache()
		C.INFO.options.clear()
		C.INFO.case('default', None)
		C.Module.reset()
		self.environ = environ
		self.start_response = start_response
		self.request = {}
		self.mod = 'HTTP_IF_MODIFIED_SINCE' in self.environ
	def create_session(self):
		C.SESSION = Session()
		if 'HTTP_COOKIE' in self.environ:
			C.SESSION.cookie.load(
				self.environ['HTTP_COOKIE']
				)
	def ok_scheme(self):
	    protocol = C.LIVE_URL.split('://')[0]
	    scheme = self.environ['wsgi.url_scheme']
	    return protocol == scheme
	def force_scheme(self):
	    return self.redirect301(C.LIVE_URL)
	@classmethod
	def set_cache(cls):
		C.USER = None
		cls.def_cache = C.Counter(
			'seconds',
			expire=int(C.EXPIRES)
			)
		cls.static_cache = C.Counter(
			'seconds',
			expire=int(C.STATIC_EXPIRES)
			)
		cls.cache_isset = True
		lastmod = cls.def_cache.header()
		cls.def_cache.lastmod = lastmod
		cls.static_cache.lastmod = lastmod
	@classmethod
	def set_lastmod(cls, cache):
		cache.lastmod = cls.def_cache.header()
	def setaction(self):
		action_isset = INFO.has('action')
		if not action_isset:
			INFO.case(
				'action',
				self.crud.address(
					self.environ[
						'REQUEST_METHOD'
						]
					)
				)
	def address(self):
		protocol = self.environ[
			'SERVER_PROTOCOL'
			].split('/')[0].lower()
		host = self.environ[
			'HTTP_HOST'
			].lower()
		path_info = self.environ[
			'PATH_INFO'
			].lower()
		self.url = Snippet(
			protocol,
			'://',
			host,
			path_info
			).string()
	def clean(self, key, string):
		if 'raw' not in key:
			string = escape(string)
		return string
	def parse_get_request(self):
		get_data = self.environ['QUERY_STRING']
		data = parse_qs(get_data)
		parse_data = {}
		[parse_data.update({
		    text(key).lower(): text(data[key][0]).lower()
		    }) for key in data]
		self.request.update(parse_data)
	def parse_post_request(self):
		try:
			request_body_size = int(
				self.environ.get(
					'CONTENT_LENGTH', 0))
		except ValueError:
			request_body_size = 0
		request_body = self.environ[
			'wsgi.input'].read(
				request_body_size)
		body = parse_qs(text(request_body))
		parse_data = {}
		[parse_data.update({
		    text(key): body[key]
		    }) for key in body]
		for key in parse_data:
			values = parse_data[key]
			if len(values) == 1:
				values = text(values[0])
			elif len(values) > 1:
			    values = [text(val) for val in values]
			parse_data[key] = values
		C.INFO.cases(**parse_data)
	def getval(self, arg):
		return self.clean(
			arg,
			self.request[arg])
	def __to_payload(self, key):
		value = self.getval(key)
		C.INFO.case(key, value)
		self.populate(value)
	def populate(self, key):
		haskey = key in self.request
		if haskey:
				self.__to_payload(key)
	def querystring(self):
		for key in self.request:
			value = self.getval(key)
			C.INFO.case(key, value)
	def kwargify(self):
		for path in self.pathlist:
			index = self.pathlist.index(path)
			new_path = escape(path)
			new_path = new_path.lower()
			self.pathlist[index] = new_path
	def delgarbage(self):
		empty_count = self.pathlist.count('')
		while empty_count > 0:
			self.pathlist.remove('')
			empty_count -= 1
	def setgeolang(self):
		lang = Snippet(
			C.DEF_LANG,
			'-',
			C.DEF_COUNTRY)
		C.LANG.case(
			'html',
			lang.element)
		element = lambda: lang.element
		C.LANG.case('og', element().replace(
			'-',
			'_'))
		C.INFO.case(
			'LANG',
			C.DEF_LANG)
	def set_mode_cases(self):
		C.MODES.ifcase(
			'web',
			Web)
		C.MODES.ifcase(
			'pythonmyadmin',
			PythonMyAdmin)
		C.MODES.ifcase(
			'favicon.ico',
			Image)
		C.MODES.ifcase(
			'image',
			Image)
		C.MODES.ifcase(
			'video',
			Video)
		C.MODES.ifcase(
			'audio',
			Audio)
		C.MODES.ifcase(
			'text',
			Text)
		C.MODES.ifcase(
			'application',
			Application)
		C.MODES.ifcase(
			'sitemap',
			C.MAP_CLASS)
	def setmode(self):
		modeval = None
		for mode in C.MODES.options:
			if mode in self.pathlist:
				modeval = mode
		if modeval == None:
			modeval = 'web'
		C.INFO.case(
			'mode',
			modeval)
		C.INFO.key = modeval
		if len(self.pathlist) == 0:
			C.INFO.case(
				modeval,
				'')
	def set_pathlist(self):
		url = self.environ.get(
			'PATH_INFO',
			'')
		self.pathlist = url.split('/')
		self.pathlist.pop(0)
		self.delgarbage()
		self.kwargify()
	def __delinfo(self, key):
		if INFO.address(key) == key:
			INFO.case(key, '')
	def info_export(self):
		for path in self.pathlist:
			C.INFO.setkey(path)
		C.INFO.foreach(self.__delinfo)
	def extract(self):
		self.set_pathlist()
		self.populate('mode')
		self.querystring()
		self.set_mode_cases()
		mode_isset = 'mode' in self.request
		if not mode_isset:
			self.setmode()
		self.info_export()
	def no_embed(self):
		C.INFO.case(
			'embed',
			'false'
			)
	def add_embed(self):
		C.INFO.case(
			'embed',
			Snippet(
				self.request['embed']
				).string()
			)
	def set_embed(self):
		embed_isset = 'embed' in self.request
		condition = IfElse(
			self.add_embed,
			self.no_embed)
		condition.action(embed_isset)
	def setlang(self):
		lang_isset = 'LANG' in self.request
		if lang_isset:
			C.DEF_LANG = self.request['LANG']
	def set_idtoken(self):
		idtoken_isset = 'idtoken' in self.request
		if idtoken_isset:
			C.INFO.case(
				'idtoken',
				Snippet(
					*self.request['idtoken']
					).string()
				)
	def set_url(self):
		bad = lambda i: isinstance(i, bytes)
		C.LIVE_URL = Path.home_url(
		    *[
			    text(i) for i in self.pathlist if bad(i)
			    ])
	def add_refer(self):
		self.address()
		redir = self.url != C.LIVE_URL
		if redir:
			Redirect.urls.case(
				self.url,
				C.LIVE_URL
				)
	def set_metadata(self):
		self.set_embed()
		self.setlang()
		self.setgeolang()
		self.set_idtoken()
		self.set_url()
	def parse_environ(self):
		self.extract()
		self.set_metadata()
		C.INFO.reset('mode')
		self.setaction()
	def interface(self):
		self.parse_get_request()
		self.parse_post_request()
		self.parse_environ()
		self.add_refer()
	def header(self, status, headers):
		self.start_response(
			status,
			headers)
	def header200(self, output):
		try:
			self.header(
				str('200 OK'),
				output.headers)
			self.actions()
			return [output.content]
		except Exception:
			Errors.log()
	def header404(self):
		content_factory = ContentFactory()
		condition = IfElse(
			lambda: C.NOT_FOUND,
			lambda: C.NOT_FOUND()
			)
		content_factory.setcontent(
			condition.value(
				C.NOT_FOUND == None
				)
			)
		content_factory.default(cache=False)
		self.header(
			str('404 NOT FOUND'),
			content_factory.headers)
		return [content_factory.content]
	def header304(self):
		self.header(
			str('304 NOT MODIFIED'),
			[(
				'Cache-Control',
				''.join([
					'max-age=',
					self.expires,
					', must-revalidate'
					])
				)])
		return []
	def static_request(self):
		text = C.INFO.has('text')
		img = C.INFO.has('image')
		return text or img
	def expired(self):
		if self.static_request():
			self.expires = C.STATIC_EXPIRES
			self.current_cache = self.static_cache
		else:
			self.expires = C.EXPIRES
			self.current_cache = self.def_cache
		return self.current_cache.auto()
	def ok_version(self):
		if self.expired():
			self.set_lastmod(self.current_cache)
		return self.environ[
			'HTTP_IF_MODIFIED_SINCE'
			] == self.current_cache.lastmod
	def cache_response(self):
		if self.ok_version():
			return self.header304()
		else:
			return self.default()
	def cache_enabled(self):
		return self.mod and C.CACHE
	def redirect(self, url, type):
		Redirect.urls.options.clear()
		self.start_response(
			type,
			[(
				str('Location'),
				url)])
		return [str('1')]
	def redirect301(self, url):
		return self.redirect(
			url,
			str(
				'301 Moved Permanently'
				)
			)
	def redirect302(self, url):
		return self.redirect(
			url,
			str(
				'302 Found'
				)
			)
	def actions(self):
		for action in C.ACTIONS:
			action()
	def load(self):
		try:
			if not C.INFO.canloop('mode'):
				C.INFO.options.clear()
				C.INFO.cases(
					**{
						'mode': 'web',
						'web': '404',
						'default': None}
					)
				raise URLError
			init_object = self.target_object()
			cont_fact = init_object.load()
			if cont_fact == None:
				raise TypeError
			return self.header200(
				cont_fact
				)
		except Exception:
			return self.header404()
	def settarget(self):
		self.mode = INFO.liveaddress()
		self.target_object = MODES.address(
			self.mode)
	def default(self):
		self.create_session()
		self.settarget()
		val = self.load()
		C.USER = None
		return val
	def forward(self):
		return self.redirect301(
			Redirect.forward(
				C.LIVE_URL
				)
			)
	def output(self):
		self.interface()
		if not self.ok_scheme():
		    return self.force_scheme()
		if Redirect.has(C.LIVE_URL):
		    self.forward()
		if self.cache_enabled():
			return self.cache_response()
		return self.default()

class Debugger(object):
    http = HTTP()
    tries = 0
    timer = Timer()
    timer.seconds = 10
    timer.bytes = 15
    @classmethod
    def init(cls, entrypoint, *env_funcs):
        for func in env_funcs:
            func()
        cls.server = make_server(
			'localhost',
			8000,
			entrypoint)
    @classmethod
    def staticinit(cls):
        File.staticinit()
        cls.init(FileFactory.wsgi)
    @classmethod
    def initmain(cls):
        cls.init(
			MAIN.application,
			MAIN.settings
			)
    @classmethod
    def staticserve(cls):
        cls.staticinit()
        cls.server.handle_request()
    @classmethod
    def staticlisten(cls):
        cls.staticinit()
        cls.server.serve_forever()
    @classmethod
    def serve(cls):
        cls.initmain()
        cls.server.handle_request()
    @classmethod
    def listen(cls):
        cls.initmain()
        cls.server.serve_forever()
    @classmethod
    def __info_from_args(
		cls,
		*args):
        WSGI(
			'',
			'').kwargify(
				*args)
    @classmethod
    def __info_from_kwargs(
		cls,
		*kwargs):
        for key in kwargs:
            C.INFO.case(
				key,
				kwargs[key])
    @classmethod
    def component_test(
		cls,
		methodName,
		*args,
		**kwargs):
        has_args = len(args) > 0
        condition = IfElse(
			cls.__info_from_args,
			cls.__info_from_kwargs)
        get_payload = condition.address(
			has_args)
        argument = Switch(
			cls.__info_from_args,
			args)
        argument.case(
			cls.__info_from_kwargs,
			kwargs)
        get_arg = argument.address(
			get_payload)
        getPayload(get_arg())
        C.INFO.reset('mode')
        method = cls.__dict__[methodName]
        self = cls()
        return method(self)
    @classmethod
    def __stoptimer(cls, inst):
        end = cls.http.length() > 0
        if end:
            inst.stop = True
    @classmethod
    def send_getrequest(cls):
        full_url = Path.fullpath(
			*cls.args,
			**cls.kwargs)
        thread.start_new_thread(
			cls.timer.start,
			(),
			{
				'iteraction':
				cls.__stoptimer})
        thread.start_new_thread(
			cls.http.get,
			(full_url,))
    @classmethod
    def init_request(cls):
        Timer.setval(
			0.5,
			lambda: cls.sendGetRequest())
        cls.print_response()
    @classmethod
    def __recurse(cls):
        fail_msg = '\nFailed\n'
        suc_msg = '\nSuccess\n'
        try_msg = '\nTrying Again...\n'
        failed = cls.http.length() == 0
        if failed:
            cls.tries += 1
        msgs = lambda: IfElse(fail_msg, suc_msg)
        getmsg = lambda: msgs().address
        print(getmsg()(failed))
        try_again = cls.tries < 3 and failed
        if try_again:
            print(try_msg)
            cls.entry_point(
				*cls.args,
				**cls.kwargs)
    @classmethod
    def __printstats(cls):
        char_count = Snippet(
			'Chars: ',
			str(
				cls.http.length()))
        getSpeed = lambda val1, val2: val1*val2
        real_speed = getSpeed(
			cls.timer.delay,
			cls.thread_ratio)
        speed = Snippet(
			str(real_speed),
			' sec'
			).string()
        print(cls.http.element)
        print(C.INFO.options)
        print(char_count.string())
        print('speed: ', speed)
        cls.__recurse()
    @staticmethod
    def __seperator(inst):
        print('\n...\n')
    @classmethod
    def print_response(cls):
        r_len = cls.http.length
        loopCount = 0
        Timer.setval(
			3,
			cls.__printstats,
			show=True,
			bytes=1,
			adjust=1,
			prtaction=cls.__seperator)
    @classmethod
    def __test(
		cls,
		*args,
		**kwargs):
        cls.args = args
        cls.kwargs = kwargs
        cls.init_request()
    @classmethod
    def sitetest(
		cls,
		*args,
		**kwargs):
        cls.thread_ratio = 1.0642954161747717
        cls.entry_point = cls.sitetest
        cls.__test(
			*args,
			**kwargs)
    @classmethod
    def localtest(
		cls,
		*args,
		**kwargs):
        args = list(args)
        args.insert(
			0,
			C.DOMAIN)
        cls.thread_ratio = 0.7982519613070302
        cls.entry_point = cls.localtest
        thread.start_new_thread(
			cls.serve,
			())
        cls.__test(
			*args,
			**kwargs)

def application(environ, start_response):
	return C.WSGI(
		environ,
		start_response
		).output()