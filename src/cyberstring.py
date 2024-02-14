# coding=utf-8

from __future__ import unicode_literals
from builtins import str
from builtins import range
from builtins import object
from sys import modules
C = modules['MAIN'].C
C.Module.module_access(
	__name__
	)

class Substring(object):
	@staticmethod
	def after(
		string,
		seperator):
		as_of = string.index(seperator) + 1
		return string[as_of:]
	@staticmethod
	def before(
		string,
		seperator):
		as_of = string.index(seperator)
		return string[:as_of]

class DataType(object):
	__data = Switch()
	@classmethod
	def __init_cases(cls):
		cls.__data.case(str, str)
		cls.__data.case(bytes, text)
		cls.__data.case(int, str)
		cls.__data.case(
			list,
			cls.__convert_list)
		cls.__data.case(
			tuple,
			cls.__convert_tuple)
		cls.__data.case(
			set,
			cls.__convert_set)
		cls.__data.case(
			frozenset,
			cls.__convert_frozen_set)
		cls.__data.case(
			dict,
			cls.__convert_dict)
		cls.__data.case(
			OrderedDict,
			cls.__convert_ordered_dict)
		cls.__data.setdefault(cls.__no_convert)
	@classmethod
	def __checkdata(cls):
		if len(cls.__data.options) == 0:
			cls.__init_cases()
	@classmethod
	def __convert(cls, data):
		conversion = cls.__conversion(type(data))
		return conversion(data)
	@classmethod
	def string(cls, data):
		cls.__checkdata()
		return text(cls.__convert(data))
	@classmethod
	def __conversion(cls, case):
		return cls.__data.defaddress(case)
	@staticmethod
	def __no_convert(item):
		return item
	@classmethod
	def __convert_assoc_array(cls, items):
		item_dict = {}
		for key in items:
			item_dict[
				cls.__convert(key)
				] = cls.string(
					items[key]
					)
		return item_dict
	@staticmethod
	def __str_dict(items):
		return str(dict(items))
	@classmethod
	def __convert_dict(cls, items):
		return cls.__str_dict(
			cls.__convert_assoc_array(items)
			)
	@staticmethod
	def __str_ordered_dict(items):
		return str(OrderedDict(items))
	@classmethod
	def __convert_ordered_dict(cls, items):
		return cls.__str_ordered_dict(
			cls.__convert_assoc_array(items)
			)
	@classmethod
	def __convert_list(cls, items):
		item_list = []
		for item in items:
			item_list.append(
				cls.string(item)
				)
		return item_list
	@classmethod
	def __convert_set(cls, items):
		return set(
			cls.__convert_list(items)
			)
	@classmethod
	def __convert_frozen_set(cls, items):
		return frozenset(
			cls.__convert_list(items)
			)
	@classmethod
	def __convert_tuple(cls, items):
		return tuple(
			cls.__convert_list(items)
			)

class Delimiter(object):
	__delimiters = Switch()
	__delimiters.case(True, '')
	__items = PyGod()
	@classmethod
	def __import(cls, current, last):
		cls.__items.current = current
		cls.__items.last = last
	@classmethod
	def __delimit(cls):
		is_last = cls.__delimiters.address(
			cls.__items.current == cls.__items.last
			)
		cls.__items.reset()
		cls.__delimiters.delcase(False)
		return is_last
	@classmethod
	def __delimiter(cls, delimiter):
		cls.__delimiters.case(
			False,
			delimiter)
	@classmethod
	def comma(cls, current, last):
		cls.__import(current, last)
		cls.__delimiter(', ')
		return cls.__delimit()
	@classmethod
	def space(cls, current, last):
		cls.__import(current, last)
		cls.__delimiter(' ')
		return cls.__delimit()
	@classmethod
	def hyphen(cls, current, last):
		cls.__import(current, last)
		cls.__delimiter(' - ')
		return cls.__delimit()
	@classmethod
	def semicolon(cls, current, last):
		cls.__import(current, last)
		cls.__delimiter('; ')
		return cls.__delimit()

class Snippet(list):
    def __init__(self, *args):
        super(
			Snippet,
			self).__init__()
        self.element = ''
        if args:
            self.join(*args)
    def add(self, element):
        self.setval(
			self.element.__add__(
				text(element)))
    def popval(self, val):
        index = self.index(val)
        self.pop(index)
    def popvals(self, val):
        while val in self:
            self.popval(val)
    def poplist(self, *args):
        [self.popvals(arg) for arg in args]
    def join(self, *args):
        self.extend(args)
        bad = lambda val: type(val) != str
        vals = [i for i in self if bad(i)]
        self.poplist(*list(set(vals)))
        self.add(''.join(self))
        del self[:]
    def insert(self, group, items):
        element = text(group) % (text(items))
        self.add(element)
    def setchar(self, char, index):
        items = list(self.string())
        items[index] = char
        self.join(*items)
    def delchar(self, index):
        self.setchar('', index)
    def reset(self):
        self.setval('')
    def has(self, substr):
        return substr in self.element
    def setval(self, element):
        self.element = text(element)
    def string(self):
        element = self.element
        self.reset()
        return element
    def replace(self, old, new):
        self.setval(
			self.string().replace(
				old, new
				)
			)
    def replaces(self, **kwargs):
        for key in kwargs:
            self.replace(key, kwargs[key])
    def filter(self, element):
        self.replace(element, '')
    def filters(self, *args):
        for arg in args:
            self.filter(arg)
    def length(self):
        return len(self.element)
    def __repr__(self):
        return ''.join([
			'Snippet(', self.element,
			') ', str(self[:])])

class Censor(object):
	word_list = []
	adult_words = []
	vulgar_words = []
	censored_text = Snippet()
	args = []
	execute = None
	__filters = Switch()
	@classmethod
	def __init_filters(cls):
		cls.__filters.case(
			'all',
			cls.__all)
		cls.__filters.case(
			'adult',
			cls.__adult)
		cls.__filters.case(
			'vulgar',
			cls.__vulgar)
		cls.__filters.case(
			'custom',
			cls.__custom)
		if cls.__filters.has(CENSOR):
			cls.execute = cls.__filters.address(CENSOR)
	@classmethod
	def reset(cls):
		del cls.word_list[:]
	@classmethod
	def __glue(cls):
		last_word = cls.word_list[
			len(cls.word_list) - 1
			]
		for word in cls.word_list:
			cls.censored_text.join(
				word,
				Delimiter.space(
					word,
					last_word
					)
				)
	@staticmethod
	def __censor(word, lowerText):
		word_length = len(word)
		chars = []
		for char in range(word_length):
			chars.append('*')
		return lowerText.replace(
			word,
			Snippet(*chars).string()
			)
	@classmethod
	def __apply_one(cls, word):
		for item in cls.word_list:
			lower_text = item.lower()
			match = word in lower_text
			if match:
				index = cls.word_list.index(item)
				cls.word_list[index] = cls.__censor(
					word,
					lower_text)
	@classmethod
	def __apply_all(cls, category):
		for word in category:
			cls.__apply_one(word)
	@classmethod
	def __adult(cls):
		cls.__apply_all(cls.adult_words)
	@classmethod
	def __vulgar(cls):
		cls.__apply_all(cls.vulgar_words)
	@classmethod
	def __custom(cls):
		cls.__apply_all(cls.args)
	@classmethod
	def __all(cls):
		cls.__adult()
		cls.__vulgar()
		cls.__custom()
	@classmethod
	def filter(cls, text):
		no_exec = cls.execute == None
		if no_exec:
			cls.__init_filters()
		cls.word_list.extend(
			text.split())
		if cls.__filters.has(CENSOR):
			cls.execute()
		cls.__glue()
		cls.reset()
		return cls.censored_text.string()