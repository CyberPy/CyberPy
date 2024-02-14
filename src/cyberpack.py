# coding=utf-8

from __future__ import unicode_literals
from builtins import str
from builtins import object
from sys import modules
C = modules['MAIN'].C
from py_compile import compile

SRC = '''
import cyberpy as C
C.FILE.reset()

class App(object):
	root = C.FILE.current_dir

	@classmethod
	def __fpath(cls, path):
		return ''.join(
			[
				cls.root,
				path
				]
			)

	@classmethod
	def __setpath(cls, path):
		C.FILE.setfile(
			cls.__fpath(path)
			)

	@staticmethod
	def __createpath():
		try:
			C.makedirs(C.FILE.current_dir)
		except OSError:
			pass

	@classmethod
	def unpack(cls):
		for path in FILES:
			cls.__setpath(path)
			cls.__createpath()
			C.FILE.binwrite(
				FILES[path]
				)

App.unpack()
C.FILE.reset()
'''

SCRIPT = ['FILES = ']

class SoftDrive(object):
	root = C.FILE.current_dir
	files = C.Switch()
	dirs = C.Switch()
	img = ('image',)
	imgs = ('images',)
	audio = ('audio',)
	video = ('video',)
	css = ('text', 'css')
	js = ('text', 'js')
	bin = ('bin',)
	min = ('min',)

	@classmethod
	def __getdir(cls, ptr, path):
		for ext in ptr.extensions:
			cls.dirs.case(ext, path)

	@classmethod
	def __gettxt(cls):
		for ext in C.Text.extensions:
			cls.dirs.case(
				'min.'.__add__(ext), 
				cls.min)
			cls.dirs.case(
				'og.'.__add__(ext),
				cls.min)

	@classmethod
	def __getimg(cls):
		cls.__getdir(
			C.Image,
			cls.img
			)
		for ext in C.Image.extensions:
			cls.dirs.case(
				'pma.'.__add__(ext), 
				cls.imgs)

	@classmethod
	def __getvid(cls):
		cls.__getdir(
			C.Video,
			cls.video
			)

	@classmethod
	def __getaudio(cls):
		cls.__getdir(
			C.Audio,
			cls.video
			)

	@classmethod
	def __getcss(cls):
		cls.dirs.case(
			'css', 
			cls.css
			)

	@classmethod
	def __getjs(cls):
		cls.dirs.case(
			'js', 
			cls.js
			)

	@classmethod
	def __getbin(cls):
		cls.dirs.case(
			'', 
			cls.bin
			)

	@classmethod
	def __getpy(cls):
		cls.dirs.case('py', ())

	@classmethod
	def __getdirs(cls):
		cls.__getpy()
		cls.__getimg()
		cls.__getvid()
		cls.__getaudio()
		cls.__getcss()
		cls.__getjs()
		cls.__getbin()
		cls.__gettxt()

	@classmethod
	def __fkey(cls):
		return C.FILE.getpath(
			).replace(cls.root, '')

	@classmethod
	def __storefile(cls):
		try:
			cls.files.case(
				cls.__fkey(),
				C.FILE.bincontent()
				)
		except OSError:
			pass
	
	@classmethod
	def __storefiles(cls, ext):
		for file in C.listdir(
			C.FILE.current_dir
			):
			lowerfile = file.lower()
			if lowerfile.endswith(ext):
				C.FILE.getfile(lowerfile)
				cls.__storefile()

	@classmethod
	def __storedir(cls, ext, *dirs):
		C.FILE.downdir(*dirs)
		try:
			cls.__storefiles(ext)
		except OSError:
			pass
		C.FILE.reset()

	@classmethod
	def __storedirs(cls):
		for ext in cls.dirs.options:
			cls.__storedir(
				ext, 
				*cls.dirs.address(ext)
				)

	@classmethod
	def __save(cls):
		cls.__getdirs()
		cls.__storedirs()

	@classmethod
	def __bytelist(cls):
		return (
			str(cls.files.options),
			'\n', SRC)

	@classmethod
	def toscript(cls):
		C.FILE.reset()
		cls.__save()
		SCRIPT.extend(
			cls.__bytelist()
			)

class App(object):
	@classmethod
	def __setpath(cls):
		C.FILE.reset()
		pathlist = C.FILE.current_dir.split('/')
		last = pathlist[len(pathlist) - 1]
		cls.appname = last.lower()
		C.FILE.getfile(
			cls.appname.__add__(
				'_cyberpack.py')
			)

	@classmethod
	def __topy(cls):
		C.FILE.binwrite(*SCRIPT)

	@staticmethod
	def __topyc():
		compile(C.FILE.current_file)
		C.remove(C.FILE.current_file)

	@classmethod
	def write(cls, pyc):
		C.FILE.getfile(
			cls.appname.__add__(
				'.cyberpack'))
		C.FILE.binwrite(pyc.content)

	@classmethod
	def __compress(cls):
		C.FILE.getfile(
			C.FILE.current_file.__add__('c')
			)
		pyc = C.ContentFactory()
		pyc.content = C.FILE.bincontent()
		pyc.compress()
		C.remove(C.FILE.getpath())
		return pyc

	@classmethod
	def pack(cls):
		cls.__setpath()
		cls.__topy()
		cls.__topyc()
		return cls.__compress()

class CyberPack(object):

	@classmethod
	def __setpath(cls):
		C.FILE.getfile(
			cls.cpk.__add__('.cyberpack')
			)

	@staticmethod
	def __bytes():
		factory = C.ContentFactory()
		factory.content = C.FILE.bincontent()
		factory.decompress()
		return factory

	@classmethod
	def __appname(cls):
		return cls.cpk.__add__(
			'_cyberpack.pyc'
			)

	@classmethod
	def __pyc(cls, appname):
		bytes = cls.__bytes()
		C.FILE.getfile(appname)
		C.FILE.binwrite(bytes.content)

	@staticmethod
	def __import(appname):
		exe = C.Snippet(
			'import ',
			appname
			)
		exe.filter('.pyc')
		exec(exe.string())

	@classmethod
	def unpack(cls):
		cls.__setpath()
		appname = cls.__appname()
		cls.__pyc(appname)
		cls.__import(appname)
		C.FILE.getfile(appname)
		C.remove(C.FILE.getpath())

def cyberpack(write=True):
	SoftDrive.toscript()
	pyc = App.pack()
	if write:
		App.write(pyc)
	return pyc

def unpack(cpk):
	C.FILE.reset()
	CyberPack.cpk = cpk
	CyberPack.unpack()