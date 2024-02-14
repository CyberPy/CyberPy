# coding=utf-8

from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
from builtins import object
from sys import modules
C = modules['MAIN'].C
C.Module.module_access(
	__name__
	)

class Errors(object):
	__stats = PyGod()
	@classmethod
	def __init_stats(cls):
		cls.__file()
		cls.__errorcode()
		cls.__glue_stats()
	@classmethod
	def __file(cls):
		stack = inspect.stack()[3]		
		file_path = stack[1]
		path_list = file_path.split('\\')
		cls.__stats.file = path_list[
			len(path_list) - 1
			]
		cls.__stats.func = stack[3]
	@classmethod
	def __errorcode(cls):
		info = exc_info()
		cls.__stats.error = str(info[0])
		cls.__stats.line = str(info[2].tb_lineno)
	@classmethod
	def __glue_stats(cls):
		cls.__stats.message = Snippet(
			'Function: ',
			cls.__stats.func,
			'\n',
			cls.__stats.error,
			'\n line: ',
			cls.__stats.line,
			' in ',
			cls.__stats.file
			).string()
	@classmethod
	def log(cls):
		cls.__init_stats()
		print(cls.__stats.message)
		cls.__stats.reset()
	def stats(self, func):
		try:
			return func()
		except Exception:
			self.__init_stats()
			err = Snippet(
				'Error in ',
				self.__stats.message
				).string()
			self.__stats.reset()
			return err
	def check_silent(self):
		has_silent = 'silent' in self.__dict__
		if not has_silent:
			self.silent = True
	def attempt(self, func):
		self.check_silent()
		try:
			func()
			return True
		except Exception:
			if not self.silent:
				self.log()
			return False