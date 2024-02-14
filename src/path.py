# coding=utf-8

from __future__ import unicode_literals
from builtins import object
from sys import modules
C = modules['MAIN'].C
C.Module.module_access(
	__name__
	)

class Path(object):
	__url = Snippet()
	@classmethod
	def __setfullpath(
		cls, 
		*args):
		for arg in args:
			cls.__url.add(arg)
			cls.__url.add('/')
	@classmethod
	def fullpath(
		cls, 
		*args, 
		**kwargs):
		cls.__setfullpath(*args)
		cls.__setparams(**kwargs)
		return cls.__url.string()
	@classmethod
	def __setrelpath(
		cls, 
		*args):
		cls.__url.add('/')
		cls.__setfullpath(*args)
	@classmethod
	def __setlastchar(
		cls, 
		character):
		index = len(cls.__url.element) - 1
		cls.__url.setchar(
			character,
			index)
	@classmethod
	def __ampersand(cls):
		cls.__setlastchar('&')
	@classmethod
	def __q_mark(cls):
		cls.__setlastchar('?')
	@classmethod
	def __add(
		cls, 
		key, 
		value):
		cls.__url.join(
			key,
			'=',
			value,
			'/')
	@classmethod
	def __append(
		cls, 
		key, 
		value):
		cls.__ampersand()
		cls.__add(key, value)
	@classmethod
	def __create(
		cls, 
		key, 
		value):
		cls.__q_mark()
		cls.__add(key, value)
	@classmethod
	def __addHeader(
		cls, 
		key, 
		value):
		has_info = '?' in cls.__url.element
		condition = IfElse(
			cls.__append, 
			cls.__create)
		action = condition.address(has_info)
		action(key, value)
	@classmethod
	def __setparams(
		cls, 
		**kwargs):
		for key in kwargs:
			cls.__addHeader(
				key,
				kwargs[key])
		cls.__set_idtoken()
	@classmethod
	def __add_idtoken(cls):
		cls.__addHeader(
			'idtoken', 
			C.INFO.address('idtoken'))
	@classmethod
	def __set_idtoken(cls):
		has_idtoken = 'idtoken' in C.INFO.options
		if has_idtoken:
			cls.__add_idtoken()
	@classmethod
	def relpath(
		cls, 
		*args, 
		**kwargs):
		cls.__setrelpath(*args)
		cls.__setparams(**kwargs)
		return cls.__url.string()
	@classmethod
	def url(
		cls, 
		domain, 
		*args, 
		**kwargs):
		cls.__url.add(domain)
		index = len(domain) - 1
		trails_dash = domain[index] == '/'
		condition = IfElse(
			cls.__setfullpath,
			cls.__setrelpath)
		action = condition.address(trails_dash)
		action(*args)
		cls.__setparams(**kwargs)
		return cls.__url.string()
	@classmethod
	def home_url(
		cls, 
		*args, 
		**kwargs):
		return cls.url(
			DOMAIN, 
			*args, 
			**kwargs)
	@classmethod
	def linkify(
		cls, 
		text, 
		path, 
		**kwargs):
		props = {'href': path}
		if kwargs:
			props.update(kwargs)
		return C.UI.create_element(
			'a',
			text,
			**props)
	@classmethod
	def __props(cls):
		props = {}
		hasrel = 'rel' in cls.kwargs
		if hasrel:
			props['rel'] = cls.kwargs['rel']
			del cls.kwargs['rel']
		hastarget = 'target' in cls.kwargs
		if hastarget:
			props['target'] = cls.kwargs['target']
			del cls.kwargs['target']
		return props
	@classmethod
	def rellink(
		cls, 
		text, 
		*args, 
		**kwargs):
		cls.kwargs = kwargs
		props = cls.__props()
		return cls.linkify(
			text, 
			cls.relpath(
				*args, 
				**cls.kwargs
				),
			**props
			)
	@classmethod
	def link(
		cls, 
		text, 
		*args, 
		**kwargs):
		cls.kwargs = kwargs
		external_domain = 'DOMAIN' in kwargs
		if external_domain:
			domain_value = kwargs['DOMAIN']
			del kwargs['DOMAIN']
		else:
			domain_value = DOMAIN
		props = cls.__props()
		return cls.linkify(
			text, 
			cls.url(
				domain_value, 
				*args, 
				**cls.kwargs), 
			**props
			)