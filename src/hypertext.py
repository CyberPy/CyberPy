# coding=utf-8

from __future__ import unicode_literals
from builtins import str
from builtins import object
from sys import modules
C = modules['MAIN'].C
C.Module.module_access(
	__name__
	)

class HyperText(object):
    text = Snippet()
    def __init__(self):
        super(
			HyperText, 
			self
			).__init__()
    @classmethod
    def tag(
		cls, 
		element, 
		string):
        cls.text.insert(element, string)
        return cls.text.string()
    @classmethod
    def tags(
		cls, 
		element, 
		*args):
        cls.text.join(*args)
        return cls.tag(
			element,
			cls.text.string())
    @classmethod
    def addprop(
		cls, 
		tag, 
		property):
        cls.text.insert('%s>', property)
        cls.text.setval(
			tag.replace(
				'>', 
				cls.text.string(), 
				1))
        return cls.text.string()
    @classmethod
    def addprops(
		cls, 
		tag, 
		*args):
        cls.text.join(*args)
        return cls.addprop(
			tag, 
			cls.text.string())
    @classmethod
    def create_prop(
		cls, 
		propName, 
		value):
        return cls.tag(
			cls.__get_tag(propName),
			value)
    @classmethod
    def create_props(
		cls, 
		**kwargs):
        props = []
        for key in kwargs:
            props.append(
				cls.create_prop(
					key, kwargs[key]))
        cls.text.join(*props)
        return cls.text.string()
    @classmethod
    def __get_tag(
		cls, 
		tagName):
        if tagName in C.HTML.__dict__:
            return C.HTML.__dict__[tagName]
        else:
            return tagName
    @classmethod
    def create_element(
		cls, 
		tagName, 
		*args, 
		**kwargs):
        tag = cls.__get_tag(tagName)
        if args:
            tag = cls.tags(
				tag, 
				*args)
        if kwargs:
            tag = cls.addprop(
				tag,
				cls.create_props(
					**kwargs))
        return tag

class Element(Snippet, HyperText):
	def __init__(self, tag, *args, **kwargs):
		super(Element, self).__init__(
			C.UI.create_element(
				tag, *args, **kwargs
				),
			)
	def prop(self, propname, value):
		self.setval(
			self.addprop(
				self.element,
				self.create_prop(propname, value)
				)
			)
	def props(self, **kwargs):
		self.setval(
			self.addprop(
				self.element,
				self.create_props(**kwargs)
				)
			)
	def __repr__(self):
		return ''.join([
			'Element(', self.element,
		   ') ', str(self[:])])