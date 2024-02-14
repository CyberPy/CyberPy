# coding=utf-8

from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from builtins import str
from builtins import range
from past.utils import old_div
from builtins import object
from sys import modules
C = modules['MAIN'].C
C.Module.module_access(
	__name__
	)

uid = lambda: str(int(time()))

class Timer(object):
    def __init__(self):
        super(
			Timer,
			self).__init__()
        self.show = False
        self.condition = IfElse(
			self.print_delay,
			ControlFlow.skip)
        self.bytes = 4
        self.livedelay = 0
        self.adjust = 0
    def get_delay(self):
        snip_time = Snippet(
			str(self.delay
	   )[:self.bytes],
			' sec')
        unit = snip_time.element[0]
        newval = int(unit) + self.adjust
        snip_time.setchar(
			str(newval),
			0)
        return snip_time.string()
    def print_delay(self):
        newdelay = self.get_delay()
        not_same = newdelay != self.livedelay
        if not_same:
            self.livedelay = newdelay
            print(newdelay)
            self.prtaction(self)
    def set_delay(self):
        self.delay = time() - self.initial
        self.action()
    def update(self):
        self.set_delay()
        self.stop = self.delay >= self.seconds
    def start(
		self,
		*ACTIONS,
		**kwargs):
        if 'iteraction' in kwargs:
            iteraction = kwargs['iteraction']
        else:
            iteraction = lambda inst: ControlFlow.skip()
        if 'prtaction' in kwargs:
            self.prtaction = kwargs['prtaction']
        else:
            self.prtaction = lambda inst: ControlFlow.skip()
        self.seconds -= 1.0
        self.action = self.condition.address(
			self.show)
        self.initial = time()
        while True:
            self.update()
            iteraction(self)
            if self.stop:
                break
        for action in ACTIONS:
            action()
    @classmethod
    def setval(
		cls,
		time,
		*ACTIONS,
		**kwargs):
        has_show = 'show' in kwargs
        timer = cls()
        if has_show:
            timer.show = kwargs['show']
            del kwargs['show']
        has_bytes = 'bytes' in kwargs
        if has_bytes:
            timer.bytes = kwargs[
				'bytes']
            del kwargs['bytes']
        has_adjust = 'adjust' in kwargs
        if has_adjust:
            timer.adjust = kwargs[
				'adjust']
            del kwargs['adjust']
        timer.seconds = time
        timer.start(
			*ACTIONS,
		    **kwargs)

class TimeStamp(object):
    weekdays = [
		'Mon', 'Tue', 'Wed',
		'Thu', 'Fri', 'Sat',
		'Sun']

    months = [
		'Jan', 'Feb', 'Mar',
		'Apr', 'May', 'Jun',
		'Jul', 'Aug', 'Sep',
		'Oct', 'Nov', 'Dec']

    def __init__(self):
        super(
			TimeStamp,
			self).__init__()
    def load(self):
        timestamp = datetime.utcnow()
        return str(timestamp)
    def __set_months(self):
        self.months = Switch()
        self.months.case(
			'01',
			'January')
        self.months.case(
			'02',
			'February')
        self.months.case(
			'03',
			'March')
        self.months.case(
			'04',
			'April')
        self.months.case(
			'05',
			'May')
        self.months.case(
			'06',
			'June')
        self.months.case(
			'07',
			'July')
        self.months.case(
			'08',
			'August')
        self.months.case(
			'09',
			'September')
        self.months.case(
			'10',
			'October')
        self.months.case(
			'11',
			'November')
        self.months.case(
			'12',
			'December')
    def get_date(
		self,
		timestamp):
        self.__set_months()
        timestamp = self.__split_stamp(
			timestamp)
        month = self.months.address(
			timestamp[1])
        return Snippet(
			month,
			' ',
			timestamp[2],
			', ',
			timestamp[0]
			).string()
    def get_datetime(
		self,
		timestamp):
        datetime = Snippet(
			self.get_date(
				timestamp),
			', at ')
        timestamp = self.__split_stamp(
			timestamp)
        hour = int(timestamp[3])
        if hour > 12:
            hour -= 12
            timestamp[3] = str(hour)
            period = 'pm'
        else:
            period = 'am'
        datetime.join(
			timestamp[3],
			':',
			timestamp[4],
			' ',
			period)
        return datetime.string()
    def get_datesec(
		self,
		timestamp):
        datetime = self.get_datetime(
			timestamp
			)
        timestamp = self.__split_stamp(
			timestamp
			)
        return Snippet(
			datetime,
			', ',
			timestamp[5],
			' secs'
			).string()
    def current_date(self):
        return self.get_date(
			self.load())
    def current_datetime(self):
        return self.get_datetime(
			self.load())
    def current_datesec(self):
        return self.get_datesec(
			self.load()
			)
    def __split_stamp(
		self,
		timestamp):
        split_timestamp = timestamp.split()
        date = split_timestamp[0]
        time = split_timestamp[1]
        split_date = date.split('-')
        split_time = time.split(':')
        year = split_date[0]
        month = split_date[1]
        day = split_date[2]
        hour = split_time[0]
        minute = split_time[1]
        second = split_time[2]
        units = [
			year, month, day,
			hour, minute, second]
        return units
    def __edit_timestamp(
		self,
		timestamp):
        split_decimals = timestamp.split('.')
        decimals = int(split_decimals[1])
        new_decimal = str(decimals + 1)
        return timestamp.replace(
			split_decimals[1],
			new_decimal)
    def __filter_time(
		self,
		stamplist,
		timestamp):
        needsedit = lambda: timestamp in stamplist
        while needsedit():
            timestamp = self.__edit_timestamp(
				timestamp)
            if not needsedit():
                break
        return timestamp
    def unique(
		self,
		stamplist):
        return self.__filter_time(
			stamplist,
			self.load())
    def __set_unit_types(self):
        self.unit_types = Switch()
        self.unit_types.case(
			'seconds',
			self.__seconds)
        self.unit_types.case(
			'minutes',
			self.__minutes)
        self.unit_types.case(
			'hours',
			self.__hours)
        self.unit_types.case(
			'days',
			self.__days)
        self.unit_types.case(
			'weeks',
			self.__weeks)
        self.unit_types.case(
			'months',
			self.__months)
        self.unit_types.case(
			'years',
			self.__years)
    def __get_difference(
		self,
		initial,
		final):
        self.__ts_difference(
			self.__split_stamp(initial),
			self.__split_stamp(final))
    def __ts_difference(
		self,
		split_initial,
		split_final):
        self.difference = []
        for unit in range(6):
            initial_unit = int(float(split_initial[unit]))
            final_unit = int(float(split_final[unit]))
            diff_unit = final_unit - initial_unit
            self.difference.append(diff_unit)
    def __product(self, *args):
        prod = 1
        for arg in args:
            prod *= arg
        return prod
    def __sum(self, *args):
        argsum = 0
        for arg in args:
            argsum += arg
        return argsum
    def __seconds(self):
        yts = self.__product(
			self.difference[0],
			12, 4, 7, 24, 3600)

        mts = self.__product(
			self.difference[1],
			4, 7, 24, 3600)

        dts = self.__product(
			self.difference[2],
			24, 3600)

        hts = self.__product(
			self.difference[3], 3600)

        min_ts = self.__product(
			self.difference[4], 60)

        secs = int(self.difference[5])

        return self.__sum(
			yts, mts, dts,
			hts, min_ts, secs)
    def __minutes(self):
        secs = self.__seconds()
        return old_div(secs, 60)
    def __hours(self):
        mins = self.__minutes()
        return old_div(mins, 60)
    def __days(self):
        hours = self.__hours()
        return old_div(hours, 24)
    def __weeks(self):
        days = self.__days()
        return old_div(days, 7)
    def __months(self):
        weeks = self.__weeks()
        return old_div(weeks, 4)
    def __years(self):
        months = self.__months()
        return old_div(months, 12)
    def time_elapsed(
		self,
		initial,
		final,
		unitType):
        self.__get_difference(
			initial, final
			)
        self.__set_unit_types()
        time = self.unit_types.value
        return int(time(unitType))
    def header(self):
        time = list(
			C.datetime.utcnow().timetuple()
			)
        day = self.weekdays[time[6]]
        month = self.months[time[1] - 1]
        for num in range(len(time)):
            time[num] = str(time[num])
        return ''.join([
			day, ', ', time[2], ' ',
			month, ' ', time[0], ' ',
			time[3], ':', time[4], ':',
			time[5], ' GMT'])

class Counter(TimeStamp):
	def __init__(self, unit, expire=None):
		super(Counter, self).__init__()
		self.expire = expire
		self.unit = unit
		self.start = self.load()
		self.tasks = []
	def time(self):
		return self.time_elapsed(
			self.start,
			self.load(),
			self.unit
			)
	def expired(self, time):
		return time > self.expire
	def __renew(self, time):
		exp = self.expired(time)
		if exp:
			for task in self.tasks:
				task()
			self.start = self.load()
		return exp
	def refresh(self, time):
		if self.expire:
			return self.__renew(time)
	def auto(self):
		return self.refresh(self.time())

C.API.custom['uid'] = uid