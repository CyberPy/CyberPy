# coding=utf-8

from __future__ import unicode_literals
from builtins import input
from builtins import str
from builtins import range
from builtins import object
from sys import modules, executable
C = modules['MAIN'].C
C.Module.module_access(
	__name__
	)

class File(object):
	def __init__(self):
		super(
			File,
			self).__init__()
		self.valid = False
		self.reset()
	def path(self, pth):
		return pth.replace('\\', '/')
	def setfile(self, pth):
		self.current_file = self.path(pth)
		self.setdir(self.current_file)
		rep = self.current_file.replace
		self.current_file = rep(
			self.current_dir, ''
			)
		self.current_file = self.current_file[
			1:]
	def setdir(self, pth):
		self.current_dir = self.path(
			OSPath.dirname(pth)
			)
	def reset(self):
		try:
			self.setfile(
				OSPath.abspath(
					C.MAIN.__file__
					)
				)
		except (NameError, AttributeError):
			self.setfile(
				OSPath.abspath(
					executable
					)
				)
		self.valid = True
	def pythonpath(self):
		SYSPath.insert(
			0,
			self.current_dir)
	def getpath(self):
		return Snippet(
			self.current_dir,
			'/',
			self.current_file
			).string()
	def read(self, permission):
		path = self.getpath()
		self.file_size = OSPath.getsize(
			path
			)
		file = open(path, permission)
		content = file.read(self.file_size)
		file.close()
		collect()
		return content
	def content(self):
		return text(self.read('r'))
	def bincontent(self):
		return self.read('rb')
	def overwrite(self, *text_list):
		path = self.getpath()
		content = Snippet()
		file = open(path, 'w')
		for text in text_list:
				content.add(
					text
					)
		self.file_size = content.length()
		if content.length() > 0:
				file.write(
					content.string()
					)
		file.close()
		collect()
	def binwrite(self, *text_list):
		path = self.getpath()
		content = []
		file = open(path, 'wb')
		content = ''.join(text_list)
		self.file_size = len(content)
		if self.file_size > 0:
				file.write(
					content
					)
		file.close()
		collect()
	def add(self, *text_list):
		path = Snippet(
			self.current_dir,
			'/',
			self.current_file
			).string()
		content = Snippet()
		file = open(path, 'w+')
		content.add(
			file.read(
				self.file_size
				)
			)
		for text in text_list:
				content.add(
					text
					)
		self.file_size = content.length()
		file.write(
			content.string()
			)
		file.close()
	def updir(self, times):
		for number in range(times):
			self.current_dir = OSPath.dirname(
				self.current_dir
				).replace('\\', '/')
	def addpath(self, path_name):
		return Snippet(
			self.current_dir,
			'/',
			path_name
			).string()
	def appendpath(self, path_name):
		self.current_dir = self.addpath(
			path_name
			)
	def downdir(self, *dir_names):
		for dir_name in dir_names:
			self.appendpath(dir_name)
	def dirpaths(self):
		return listdir(
			self.current_dir
			)
	def lowerpaths(self):
		return [
			path.lower() for path in self.dirpaths()
			]
	def exists(self):
		try:
			lowname = self.current_file.lower()
			return lowname in self.lowerpaths()
		except:
			return False
	def validpath(self, *args):
		self.downdir(*args)
		try:
			return len(listdir(
				self.current_dir
				)) > 0
		except:
			return False
	def getfile(self, file_name):
		self.current_file = file_name
		if not self.exists():
			self.overwrite()
	def delete(self):
		remove(self.getpath())
	@classmethod
	def cfile(cls):
		C.FILE = cls()
		if C.FILE.valid:
			C.FILE.pythonpath()
	@staticmethod
	def hasindex():
		C.FILE.current_file = 'index.html'
		return C.FILE.exists()
	@staticmethod
	def has404():
		C.FILE.current_file = '404.html'
		return C.FILE.exists()
	@staticmethod
	def createindex():
		C.FILE.overwrite(
			'''<!doctype html><html><head>
			<title>Index</title>
			</head><body><h1>
			202 | Ok
			</h1></body></html>'''
			)
		C.FILE.reset()
	@staticmethod
	def err404():
		C.FILE.overwrite(
			'''<!doctype html><html><head>
			<title>Error</title>
			</head><body><h1>
			404 | Page Not Found
			</h1></body></html>'''
			)
		C.FILE.reset()
	@classmethod
	def staticinit(cls):
		if not cls.hasindex():
			cls.createindex()
		if not cls.has404():
			cls.err404()

File.cfile()

class CodeEditor(File):
	def __init__(self):
		if C.FILE.valid:
			super(CodeEditor, self
			).__init__()
	def edit(self, *args, **kwargs):
		code = self.bincontent()
		for arg in args:
			code = arg(code)
		for key in kwargs:
			code = code.replace(
				str(key),
				str(kwargs[key])
				)
		self.binwrite(code)

class CodeBase(object):
	def __init__(self, *args):
		if C.FILE.valid:
			super(CodeBase, self
				).__init__()
			self.files = [CodeEditor()]
			self.extensions = []
			self.extensions.extend(args)
	def __path(self, folder, item):
		return ''.join([
			folder, '/', item
			])
	def __listpath(self, folder):
		dirs = listdir(folder)
		for index in range(len(dirs)):
			dirs[index] = self.__path(
				folder, dirs[index]
				)
		return dirs
	def __get_file(self, path):
		editor = CodeEditor()
		editor.setfile(path)
		return editor
	def __valid_file(self, path):
		valid = False
		split_path = path.split('/')
		file_name = split_path[-1]
		file_name = file_name.replace(
			'.min', '')
		if '.' in file_name:
			ext = Substring.after(file_name, '.')
			valid = ext in self.extensions
		return valid
	def __can_edit(self, path):
		is_valid = self.__valid_file(path)
		not_file = path != C.FILE.current_file
		return is_valid and not_file
	def __add_file(self, path):
		self.files.append(
			self.__get_file(path)
			)
	def get_files(self):
		dirs = [C.FILE.current_dir]
		index = 0
		while index < len(dirs):
			dir = dirs[index]
			try:
				dirs.extend(self.__listpath(dir))
			except:
				if self.__can_edit(dir):
					self.__add_file(dir)
			index += 1
	def edit(self, *args, **kwargs):
		main = C.FILE.getpath()
		for file in self.files:
			if file.getpath() != main:
				try:
					file.edit(*args, **kwargs)
				except:
					C.Errors.log()
					eval(input())