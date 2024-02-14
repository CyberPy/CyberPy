# coding=utf-8

from __future__ import unicode_literals
from builtins import next
from builtins import range
from builtins import object
from sys import modules
C = modules['MAIN'].C
C.Module.module_access(
	__name__
	)

def joinfuncs(*args):
	def funcs():
		val = None
		for arg in args:
			val = arg()
		return val
	return funcs

class Bool(object):

	@staticmethod
	def orsumvals(*args):
		sum = False
		for arg in args:
			sum = sum or arg
		return sum

	@classmethod
	def orsumfuncs(cls, *args):
		boollist = []
		for arg in args:
			boollist.append(arg())
		return cls.orsumvals(*boollist)

	@classmethod
	def orsum(cls, *args):
		return lambda: cls.orsumfuncs(*args)

	@staticmethod
	def andsumvals(*args):
		sum = True
		for arg in args:
			sum = sum and arg
		return sum

	@classmethod
	def andsumfuncs(cls, *args):
		boollist = []
		for arg in args:
			boollist.append(arg())
		return cls.andsumvals(*boollist)

	@classmethod
	def andsum(cls, *args):
		return lambda: cls.andsumfuncs(*args)

class ControlFlow(object):
    def __init__(self):
        super(
			ControlFlow,
			self).__init__()
        self.options = {}
    def case(self, state, value):
        self.options.update(
			{
				state:
				value
				}
			)
    def ifcase(self, state, value):
        if not self.has(state):
            self.case(state, value)
    def has(self, state):
        return state in self.options
    def delcase(self, state):
        del self.options[state]
    def ifdel(self, state):
        if self.has(state):
            self.delcase(state)
    def address(self, state):
        value = self.options[state]
        return value
    def ifaddress(self, state):
        if self.has(state):
            return self.address(state)
    def value(self, state):
        return self.address(state)()
    def ifvalue(self, state):
        if self.has(state):
            return self.value(state)
    def action(self, state):
        self.address(state)()
    def ifaction(self, state):
        if self.has(state):
            self.action(state)
    def item(self, state):
        return {
			state:
			self.address(state)}
    def empty(self):
        self.options.clear()
    @staticmethod
    def skip(*args, **kwargs):
        pass

class IfElse(ControlFlow):
    def __init__(
		self,
		true_val,
		false_val):
        super(
			IfElse,
			self).__init__()
        self.case(
			True,
			true_val)
        self.case(
			False,
			false_val)

class Switch(ControlFlow):
    def __init__(self, **kwargs):
        super(
			Switch,
			self
			).__init__()
        if kwargs:
            self.cases(**kwargs)
    def __check_key(self, key):
        if not self.has(key):
            raise KeyError
    def length(self, key):
        self.__check_key(key)
        index = 0
        while True:
            index += 1
            key = self.address(key)
            if not self.has(key):
                index += 1
                break
        return index
    def foreach(self, func):
        for key in self.options:
            func(key)
    def cases(self, **kwargs):
        self.options.update(kwargs)
    def setdefault(self, value):
        self.case(
			'default',
			value)
    def __defkey(self, key):
        haskey = self.has(key)
        hasdef = self.has('default')
        try:
            if not hasdef:
                raise KeyError
            condition = IfElse(
				key,
				'default')
            return condition.address(haskey)
        except:
            Errors.log()
    def defaction(self, key):
        self.action(
			self.__defkey(key))
    def defvalue(self, key):
        return self.value(
			self.__defkey(key))
    def defaddress(self, key):
        return self.address(
			self.__defkey(key))
    def defitem(self, key):
        item = lambda: self.item(key)
        noItem = lambda: None
        condition = IfElse(
			item,
			noItem)
        haskey = self.has(key)
        return condition.value(haskey)

class CursorSwitch(Switch):
	def __init__(self, **kwargs):
		super(
			CursorSwitch,
			self).__init__()
		self.options = OrderedDict()
		self.setdefault(None)
		self.key = 'default'
		if kwargs:
			self.cases(**kwargs)
	def canloop(self, key):
		can = True
		keylist = []
		while self.has(key):
			keylist.append(key)
			key = self.address(key)
			can = key not in keylist
			if not can or not self.has(key):
				break
		return can
	def __keylist(self, key):
		keylist = []
		while True:
			keylist.append(key)
			key = self.address(key)
			if key in keylist:
				break
			if not self.has(key):
				keylist.append(key)
				break
		return keylist
	def __commit(self, keylist, default):
		self.options.clear()
		self.fromlist(keylist)
		if default:
			self.options.update(default)
	def __cutlist(self, limit, delete, keylist):
		length = len(keylist)
		if limit:
			if length > limit:
				delete = length - limit
		if delete:
			keylist = keylist[: delete * -1]
		return keylist
	def __extras(self, keylist):
		extras = {}
		for key in self.options:
			if key not in keylist:
				extras.update(self.item(key))
		return extras
	def trim(self, key, delete=0, limit=None):
		self._Switch__check_key(key)
		default = None
		if self.has('default'):
			default = self.item('default')
		keylist = self.__keylist(key)
		extras = self.__extras(keylist)
		cutlist = self.__cutlist(
			limit, delete, keylist
			)
		self.__commit(cutlist, default)
		self.cases(**extras)
	def setcursor(self, index):
		self.key = list(self.options.items(
			))[index][0]
	def resetcursor(self):
		self.setcursor(0)
	def reset_default(self):
		self.setdefault(None)
	def setkey(self, value):
		self.case(
			self.key,
			value)
		next(self)
		self.reset_default()
	def setval(self, value):
		self.case(self.key, value)
	def liveitem(self):
		return self.defitem(
			self.key)
	def __next__(self):
		self.key = self.liveaddress()
	def nextval(self, value):
		next(self)
		self.setval(value)
	def move(self, index):
		for i in range(index):
			next(self)
	def hasnext(self):
		return self.has(
			self.liveaddress()
			)
	def tolist(self, key):
		keylist = []
		has_key = lambda: self.has(key)
		while has_key():
			key = self.address(key)
			keylist.append(key)
			if not has_key():
				break
		return keylist
	def livelist(self):
		return self.tolist(self.key)
	def last(self, key):
		keylist = self.tolist(key)
		index = len(keylist) - 1
		return keylist[index]
	def lastkey(self, key):
		keylist = self.tolist(key)
		index = len(keylist) - 2
		return keylist[index]
	def fromlist(self, items):
		items_length = len(items) - 1
		has_next = lambda val: val < items_length
		for index in range(items_length):
			if has_next(index):
				self.case(
					items[index],
					items[index + 1]
					)
			else:
				break
	def delkey(self):
		key = self.key
		next(self)
		self.delcase(key)
	def delthis(self):
		self.delcase(self.key)
	def liveaddress(self):
		return self.defaddress(
			self.key)
	def livevalue(self):
		return self.defvalue(
			self.key)
	def liveaction(self):
		self.defaction(
			self.key)
	def reset(self, firstkey):
		self.key = firstkey
		new = OrderedDict()
		valid = lambda: self.liveaddress() != None
		while valid():
			item = self.liveitem()
			new.update(item)
			self.delkey()
			if not valid():
				break
		for key in self.options:
			new[key] = self.address(key)
		self.options = new
		self.key = firstkey