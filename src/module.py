# coding=utf-8

from __future__ import unicode_literals
from builtins import object
from types import ModuleType
from sys import modules
from os.path import dirname, abspath

if 'main' in modules:
	MAIN = modules['main']
else:
	import __main__ as MAIN
modules['MAIN'] = MAIN

class Module(object):
	__package = 'cyberpy'
	@staticmethod
	def has(ref):
		return ref in MAIN.C.__dict__
	@staticmethod
	def __get_modules():
		mods = []
		for var in MAIN.C.__dict__:
			is_mod = isinstance(
				MAIN.C.__dict__[var],
				ModuleType
				)
			if is_mod:
				mods.append(var)
		return mods
	@staticmethod
	def __get_globals():
		globs = []
		for var in MAIN.C.__dict__:
			is_global = var.isupper()
			if is_global:
				globs.append(var)
		return globs
	@staticmethod
	def __set_global(glob_name, mod_name):
		mod = MAIN.C.__dict__[mod_name]
		setattr(
			mod, 
			glob_name, 
			MAIN.C.__dict__[
				glob_name
				]
			)
	@classmethod
	def update(cls):
		mods = cls.__get_modules()
		globs = cls.__get_globals()
		for mod_name in mods:
			for glob_name in globs:
				cls.__set_global(
					glob_name,
					mod_name)
		MAIN.C.collect()
	@classmethod
	def reset(cls):
		MAIN.settings()
		cls.update()
	@classmethod
	def glob(cls, glob_name, glob):
		MAIN.C.__dict__[
			glob_name
			] = glob
		mods = cls.__get_modules()
		for mod_name in mods:
			cls.__set_global(
				glob_name,
				mod_name)
	@classmethod
	def module_access(cls, module_name):
		module = modules[module_name]
		for global_key in cls.C.__dict__:
			setattr(
				module, 
				global_key, 
				cls.C.__dict__[
					global_key
					]
				)
	@classmethod
	def main_access(cls, C):
		MAIN.C = modules[C]
		cls.glob('MAIN', MAIN)
		cls.C = modules[C]