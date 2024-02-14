# coding=utf-8

from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
from builtins import range
from sys import modules
C = modules['MAIN'].C
C.Module.module_access(
	__name__
	)

class Callable(Snippet):
	def __init__(
		self, 
		keyword, 
		name, 
		*args):
		super(
			Callable, 
			self).__init__(
				keyword,
				name,
				'(')
		self.name = name
		self.indent = 0
		if args:
			last = args[-1]
			for arg in args:
				self.join(
					arg,
					Delimiter.comma(
						arg, 
						last))
		self.add(')')
		self.exp(
			':', 
			call=self.indent,
			i=1)
	def indent_all(self):
		self.setval(
			self.element.replace(
				'\n', 
				'\n\t'))
		self.indent()
	def indent(self):
		self.indent += 1
	def unindent(self):
		self.indent -= 1
	def exp(self, expression, **kwargs):
		if kwargs:
			for i in range(kwargs['i']):
				kwargs['call']()
		self.add(expression)
		self.add('\n')
		for i in range(self.indent):
			self.add('\t')
	def explist(self, *args):
		for arg in args:
			self.exp(arg)
	def compile(self):
		exec(self.element)
		self.Exec = eval(self.name)

class Function(Callable):
	def __init__(
		self, 
		name, 
		*args):
		super(
			Function, 
			self).__init__(
				'def ', 
				name, 
				*args)

class Method(Function):
	def __init__(
		self, 
		name, 
		*args, 
		**kwargs):
		super(
			Function, 
			self).__init__(
				'def ', 
				name, 
				*args)
		if kwargs:
			copy = self.string()
			self.exp(kwargs['methodType'])
			self.add(copy)
		self.indent_all()

class Class(Callable):
	def __init__(
		self, 
		name, 
		parent):
		super(
			Class, 
			self).__init__(
				'class ', 
				name, 
				parent)
	def create_method(
		self, 
		name, 
		*args, 
		**kwargs):
		self.method = Method(
			name, 
			*args, 
			**kwargs)
	def add_method(self):
		self.exp(self.method.element)
		self.method = None

class CyberObject(PyGod):

	def __init__(self):
		super(
			CyberObject, 
			self
			).__init__()

	def set(self, ref, val):
		self.__dict__[ref] = val

	def get(self, ref):
		return self.__dict__[ref]

	@staticmethod
	def log(string):
		print(string)

	def unset(self, ref):
		del self.__dict__[ref]

	def __repr__(self):
		return C.Snippet(
			'CyberObject ', 
			str(self.__dict__)
			).string()

class NameSpace(CyberObject):
	def __init__(
		self, 
		ref, 
		scope=modules[
			'MAIN'
			].__dict__
		):
		super(
			NameSpace, 
			self
			).__init__()
		scope[ref] = self

	def __repr__(self):
		return C.Snippet(
			'NameSpace ', 
			str(self.__dict__)
			).string()