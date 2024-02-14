# coding=utf-8

from __future__ import division
from __future__ import unicode_literals
from builtins import range
from builtins import object
from past.utils import old_div
from sys import modules
C = modules['MAIN'].C
C.Module.module_access(
	__name__
	)

class Divider(object):

	class SignError(ValueError):
		def __init__(self):
			super(
				Divider.SignError, self
				).__init__(
					'Not divisible by less than 1'
					)

	class DivisorError(ValueError):
		def __init__(self):
			super(
				Divider.DivisorError, self
				).__init__('Not divisible')

	@classmethod
	def __check_sign(cls, num):
		if num < 1:
			raise cls.SignError

	@classmethod
	def __check_divisor(cls, iter, num):
		if len(iter) % num:
			raise cls.DivisorError

	@classmethod
	def __div(cls, iter, num):
		pieces = old_div(len(iter), num)
		ran = [
			pieces * i for i in range(num)
			]
		return [
			iter[i:i+pieces] for i in ran
			]

	@classmethod
	def split(cls, iter, num):
		cls.__check_sign(num)
		cls.__check_divisor(iter, num)
		return cls.__div(iter, num)

class Limiter(object):
	__limited_list = []
	__initial_list = []
	__limits = PyGod()
	@classmethod
	def __length(cls):
		return len(cls.__initial_list)
	@classmethod
	def __nolimit(cls):
		return cls.__length()
	@classmethod
	def __newlist(cls):
		cls.__limits.reset()
		del cls.__initial_list[:]
		new = list(cls.__limited_list)
		del cls.__limited_list[:]
		return new
	@classmethod
	def __setlimits(cls, start, end):
		if start == 0:
			start += 1
		cls.__limits.start = start - 1
		not_end = lambda: cls.__length() < end
		endlimit = lambda: end
		condition = IfElse(
			cls.__nolimit,
			endlimit)
		cls.__limits.end = condition.value(not_end())
	@classmethod
	def __generate(cls):
		for i in range(
			cls.__limits.start, 
			cls.__limits.end):
			cls.__limited_list.append(
				cls.__initial_list[i]
				)
	@classmethod
	def limit(
		cls, 
		ordered, 
		start, 
		end):
		cls.__initial_list = ordered
		cls.__setlimits(start, end)
		cls.__generate()
		return cls.__newlist()
