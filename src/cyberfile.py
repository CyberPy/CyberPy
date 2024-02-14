# coding=utf-8

from __future__ import unicode_literals
from builtins import next
from builtins import str
from builtins import object
from sys import modules
C = modules['MAIN'].C
C.Module.module_access(
	__name__
	)

class ContentFactory(object):
	header_template = []
	def __init__(self, **kwargs):
		if not 'encoding' in kwargs:
			self.encoding = False
		else:
			self.encoding = kwargs['encoding']
		self.set_headers()
	def set_headers(self):
		self.headers = []
		self.headers.extend(
			self.header_template)
		del self.header_template[:]
		self.session()
	def session(self):
		if not C.Module.has('SESSION'):
			return None
		if C.SESSION:
			C.SESSION.set()
			self.headers.extend(
				C.SESSION.cookies)
	def lastmod(self, cache):
		if C.WSGI.cache_isset:
			self.headers.append(
				(
					'Last-Modified',
					str(cache.lastmod)
					)
				)
	def cache(self, cache_control):
		self.headers.append(
			(
				'Cache-Control',
				str(cache_control)
				)
			)
	def cache_template(self, expires):
		self.cache(''.join([
				'public, max-age=',
				expires,
				', must-revalidate'])
			 )
	def def_static_cache(self):
		self.cache_template(
			C.STATIC_EXPIRES
			)
	def def_cache(self):
		self.cache_template(C.EXPIRES)
	def no_cache(self):
		self.cache(
			'no-cache, no-store, must-revalidate'
			)
	def replace(self, new, *args):
		for arg in args:
			has = arg in self.content
			while has:
				self.content = self.content.replace(
					arg, new)
				has = arg in self.content
	def min_HTML(self):
		not_same = C.LOCAL_DOM != C.DOMAIN
		if C.LOCALHOST and not_same:
			self.replace(C.LOCAL_DOM, C.DOMAIN)
		if not C.DEV_MODE:
			self.replace('', '\n', '\t')
			self.replace('\n', '//-')
			double_space = '  ' in self.content
			while double_space:
				self.content = self.content.replace(
					'  ',
					' ')
				double_space = '  ' in self.content
				C.collect()
	def __minchars(self, *args):
		for arg in args:
			left = Snippet(' ', arg).string()
			right = Snippet(arg, ' ').string()
			self.replace(arg, left, right)
	def min(self):
		if not C.DEV_MODE:
			self.min_HTML()
			self.__minchars(
				']', '[', '{',
				'}', '=', '(',
				')', '+', '-',
				'*', '/', ';',
				':', '<', '>',
				',', '|')
			self.replace(' ', '//_')
			C.collect()
	def setcontent(
		self,
		content):
		self.content = text(content)
	def decompress(self):
		raw_bytes = BytesIO(self.content)
		gzip_file = GzipFile(
			fileobj=raw_bytes,
			mode='rb')
		self.content = gzip_file.read()
		gzip_file.close()
	def compress(self, level=9):
		raw_bytes = BytesIO()
		gzip_file = GzipFile(
			fileobj=raw_bytes,
			mode='wb',
			compresslevel=level)
		gzip_file.write(untext(self.content))
		gzip_file.close()
		self.content = raw_bytes.getvalue()
	def gzip(self):
		self.compress()
		self.encoding = 'gzip'
		self.contentencoding()
	def contenttype(
		self,
		filetype,
		extension):
		header = Snippet(
			filetype,
			'/',
			extension)
		self.headers.append((
			'content-type',
			str(header.string())))
	def contentlength(self):
		self.headers.append((
			'content-length',
			str(len(self.content))))
	def contentencoding(self):
		self.headers.append((
			'content-encoding',
			str(self.encoding)))
	def default(self, cache=True):
		if cache:
			self.def_cache()
		else:
			self.no_cache()
		self.contenttype(
			'text',
			'html; charset=UTF-8')
		self.min_HTML()
		self.gzip()

class Media(File):
    def __init__(self, auto=True):
        super(
			Media,
			self).__init__()
        self.current_dir = FILE.current_dir
        C.INFO.key = 'mode'
        if C.INFO.liveaddress() == 'web':
            next(C.INFO)
        self.mediatype = C.INFO.liveaddress()
        if auto:
            self.locate()
    def locate(self):
        self.path = C.INFO.livelist()
        self.current_file = self.path.pop(
			len(self.path) - 1
			)
        self.downdir(*self.path)
    def __ext(self):
        if '.min' in self.current_file:
            file = self.current_file.replace(
				'.min', ''
				)
        else:
            file = self.current_file
        return Substring.after(file, '.')
    def create(self):
        try:
            self.extension = self.__ext()
            okmin = self.mediatype == 'text'
            file = ContentFactory()
            file.lastmod(C.WSGI.static_cache)
            file.def_static_cache()
            file.content = self.bincontent()
            file.contenttype(
				self.mediatype,
				self.extension)
            if okmin:
                file.content = text(file.content)
                file.min()
            nocompress = ('jpg', 'jpeg')
            ok_gzip = self.extension not in nocompress
            if ok_gzip:
                file.gzip()
            return file
        except Exception:
            Errors.log()
    def load(self):
        if self.exists():
            return self.create()

class Application(Media):
	extensions = [
		'octet-stream',
		'postscript',
		'json', 'ecmascript',
		'pdf', 'zip',
		'x-bytecode.python',
		'x-shockwave-flash',
		'xml', 'x-gzip']
	def __init__(self, **kwargs):
		super(
			Application,
			self
			).__init__(**kwargs)

class Text(Media):
	extensions = [
			'txt', 'xml',
			'html', 'js',
			'css', 'x-script.phyton',
			'htm', 'plain']
	def __init__(self, **kwargs):
		super(
			Text,
			self
			).__init__(**kwargs)
	def contenttype(
		self,
		filetype,
		ext):
		header = Snippet(
			filetype,
			'/',
			'javascript' if ext == 'js' else ext)
		self.headers.append((
			'content-type',
			str(header.string())))

class Video(Media):
    extensions = [
			'webm', 'ogv',
			'ogg', 'gif',
			'mov', 'qt',
			'asf', 'mp4',
			'm4p', 'm4v',
			'mpg', 'mpeg',
			'flv']
    def __init__(self, **kwargs):
        super(
			video,
			self
			).__init__(**kwargs)

class Audio(Media):
	extensions = [
		'mp3', 'ogg',
		'm4a', 'webm',
		'wav', 'wma',
		'm4p', 'm4b']
	def __init__(self, **kwargs):
		super(
			Audio,
			self
			).__init__(**kwargs)

class Image(Media):
    extensions = [
		'jpg', 'jpeg',
		'bmp', 'png',
		'ico']
    def __init__(self, **kwargs):
        super(
			Image,
			self
			).__init__(**kwargs)

class FileFactory(object):
	medias = [
		Application, Text,
		Video, Audio, Image
		]
	def __init__(self):
		INFO.key = 'mode'
		self.media = None
		self.setmedia()
	def mediatype(self):
		return self.media.__name__.lower()
	def extension(self):
		last = INFO.last('mode')
		if not '.' in last:
			INFO.case(last, 'index.html')
			last = 'index.html'
		return Substring.after(last, '.')
	def setmedia(self):
		index = 0
		ext = self.extension()
		while True:
			exts = self.medias[index].extensions
			if ext in exts:
				self.media = self.medias[index]
				break
			index += 1
			if index > 4:
				break
	def content(self):
		media = self.media(auto=False)
		media.mediatype = self.mediatype()
		media.path = []
		media.locate()
		return media.load()
	def load(self):
		func = self.options.address(
			self.media == None
			)
		return func(self)
	@staticmethod
	def nfpage():
		page = File()
		page.getfile('404.html')
		return page.content()
	@classmethod
	def notfound(cls):
		try:
			return cls.nfpage()
		except:
			return ''
	@classmethod
	def wsgi(cls, environ, start_response):
		wsgi = C.WSGI(environ, start_response)
		C.MODES.case('web', cls)
		C.NOT_FOUND = cls.notfound
		return wsgi.output()

FileFactory.options = IfElse(
	lambda self: None,
	FileFactory.content
	)