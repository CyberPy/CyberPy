# coding=utf-8

# PyGod V1.1 (c) 2024 AristoTech*
# https://aristotech.vip/wp-content/god-1.1.py
# License: MIT
# * V1.0  published under CyberPy

# for compatibility
from __future__ import unicode_literals
from builtins import str
from builtins import object
from sys import modules
C = modules['MAIN'].C
C.Module.module_access(__name__)

class PyGod(object):
	def __init__(self, *args):
		super(
			PyGod, 
			self).__init__()
		self.foreign_objects = {}
		self.foreign_classes = {}
		self.foreign_methods = {}
		self.__unknowns = {
			True: self.import_class,
			False: self.import_object
			}
		self.import_unknowns(*args)
	def import_dict(self, py_dict):
		self.__dict__.update(py_dict)
	def has(self, prop):
		return prop in self.__dict__
	def __store_class(
		self, 
		key, 
		__class__):
		self.foreign_classes.update(
			{key:__class__}
			)
	def __store_object(self, obj):
		key = obj.__class__
		has_class = key in self.foreign_objects
		if not has_class:
			self.foreign_objects.update(
				{obj.__class__:obj}
				)
	def __store_method(
		self, 
		key, 
		method):
		self.foreign_methods.update(
			{key:method}
			)
	def __add_defaults(self):
		def_len = len(
			self.argspec.defaults)
		args_len = len(
			self.argspec.args)
		index = args_len - def_len
		for arg in self.argspec.defaults:
			self.argspec.args[
				index
				] = ''.join([
					self.argspec.args[
						index
						],
					'=',
					arg
					])
	def __add_args(self):
		self.argspec.args.append(
			''.join([
				'*',
				self.argspec.varargs
				]))
	def __add_kwargs(self):
		self.argspec.args.append(
			''.join([
				'**',
				self.argspec.varargs
				]))
	def __set_params(self):
		if self.argspec.defaults != None:
			self.__add_defaults()
		if self.argspec.varargs != None:
			self.__add_args()
		if self.argspec.keywords != None:
			self.__add_kwargs()
	def __inspect_func(
		self, 
		key, 
		func):
		self.__store_method(
			key, 
			func)
		getargs = inspect.getargspec
		self.argspec = getargs(func)
		self.__set_params()
	def __call(self, key):
		template = [
			'\n\tval = __func__(',
			'self.foreign_objects',
			'[__class__]']
		for arg in self.argspec.args:
			template.append(',')
			template.append(arg)
		template.append(')')
		return ''.join(template)
	def __def_func(self, key):
		template = [
			'def ', 
			key, 
			'( ']
		for arg in self.argspec.args:
			template.append(arg)
			template.append(',')
		template[
			len(template) - 1
			] = '):\n'
		self.argspec.args.pop(0)
		return''.join(template)
	def __func_str(self, key):
		template = [
			self.__def_func(key),
			'\n\tkey = "', key, '"',
			'\n\t__class__ = ',
			'self.foreign_classes[key]',
			'\n\t__func__ = ',
			'self.foreign_methods[key]',
			self.__call(key),
			'\n\tself.import_dict(',
			'self.foreign_objects',
			'[__class__].__dict__)',
			'\n\tself._sync_parents()',
			'\n\treturn val']
		return ''.join(template)
	def __create_method(
		self, 
		obj, 
		key, 
		func):
		self.__inspect_func(
			key, 
			func)
		exec(self.__func_str(key))
		return eval(key)
	def __bind_method(
		self, 
		key, 
		method):
		bound_method = MethodType(
			method,
			self)
		self.__dict__.update(
			{
				key:
				bound_method
				}
			)
	def __import_method(
		self, 
		obj, 
		key, 
		prop):
		self.__store_object(obj)
		self.__store_class(
			key,
			obj.__class__)
		method = self.__create_method(
			obj,
			key,
			prop)
		self.__bind_method(
			key,
			method)
	def __import_methods(self, obj):
		props = obj.__class__.__dict__
		for key in props:
			prop = props[key]
			prop_type = str(type(prop))
			func = 'function' in prop_type
			not_init = key != '__init__'
			not_repr = key != '__repr__'
			is_valid = not_init and not_repr
			is_method = func and is_valid
			if is_method:
				self.__import_method(
					obj, 
					key, 
					prop)
	def __import_parents(self, obj):
		for base in obj.__class__.__bases__:
			if base != object:
				self.__import_methods(
					base())
	def _sync_parents(self):
		for parent in self.foreign_objects:
			self.foreign_objects[
				parent
				].__dict__.update(
				self.__dict__)
	def import_object(self, obj):
		self.import_dict(
			obj.__dict__)
		self.__import_methods(obj)
		self.__import_parents(obj)
		self._sync_parents()
	def import_unknown(self, unknown):
		action = self.__unknowns[
			type(PyGod) == type(unknown)
			]
		action(unknown)
	def import_unknowns(self, *args):
		for arg in args:
			self.import_unknown(arg)
	def import_objects(self, *args):
		for arg in args:
			self.import_object(arg)
	def import_class(self, __class__):
		self.import_object(
			__class__())
	def import_classes(self, *args):
		for arg in args:
			self.import_class(arg)
	def reset(self):
		self.__dict__ = {}
		self.foreign_objects = {}
		self.foreign_classes = {}
		self.foreign_methods = {}
	def __repr__(self):
		__objects__ = ['PyGod\n{']
		for __class__ in self.foreign_objects:
			__objects__.append(''.join([
				'\n\t', 
				__class__.__name__,
				';']))
		__objects__.append('\n}\n')
		return ''.join(__objects__)