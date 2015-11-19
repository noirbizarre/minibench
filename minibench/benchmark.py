# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time
import sys

from collections import namedtuple

from .utils import humanize

DEFAULT_TIMES = 5


if sys.platform == "win32":
    # On Windows, the best timer is time.clock()
    timer = time.clock
else:
    # On most other platforms the best timer is time.time()
    timer = time.time

#: Store a single method execution result
RunResult = namedtuple('RunResult', ('duration', 'success', 'result'))


class Result(object):
    ''' Store an aggregated result for a single method'''
    def __init__(self):
        self.total = 0
        self.has_success = False
        self.has_errors = False
        self.error = None


class Benchmark(object):
    '''Base class for all benchmark suites'''
    times = DEFAULT_TIMES

    def __init__(self, times=None, prefix="bench_", debug=False,
                 before=None, before_each=None,
                 after=None, after_each=None,
                 **kwargs):

        self.times = times or self.times
        self.results = {}
        self.debug = debug

        self._prefix = prefix

        self._before = before or self._noop
        self._before_each = before_each or self._noop
        self._after = after or self._noop
        self._after_each = after_each or self._noop

    @property
    def label(self):
        '''A human readable label'''
        if self.__doc__ and self.__doc__.strip():
            return self.__doc__.strip().splitlines()[0]
        return humanize(self.__class__.__name__)

    def label_for(self, name):
        '''Get a human readable label for a method given its name'''
        method = getattr(self, name)
        if method.__doc__ and method.__doc__.strip():
            return method.__doc__.strip().splitlines()[0]
        return humanize(name.replace(self._prefix, ''))

    def _noop(self, *args, **kwargs):
        pass

    def before_class(self):
        '''Hook called before each class'''
        pass

    def before(self):
        '''Hook called once before each method'''
        pass

    def before_each(self):
        '''Hook called before each method'''
        pass

    def after_each(self):
        '''Hook called after each method once'''
        pass

    def after(self):
        '''Hook called once after each method'''
        pass

    def after_class(self):
        '''Hook called after each class'''
        pass

    def _collect(self):
        return [test for test in dir(self) if test.startswith(self._prefix)]

    def _run_one(self, func):
        self.before_each()
        tick = timer()
        success = True
        try:
            result = func()
        except Exception as e:
            success = False
            result = e
        duration = timer() - tick
        self.after_each()
        return RunResult(duration, success, result)

    def run(self):
        '''
        Collect all tests to run and run them.

        Each method will be run :attr:`Benchmark.times`.
        '''
        tests = self._collect()

        if not tests:
            return

        self.times
        self.before_class()

        for test in tests:
            func = getattr(self, test)
            results = self.results[test] = Result()
            self._before(self, test)
            self.before()
            for i in range(self.times):
                self._before_each(self, test, i)
                result = self._run_one(func)
                results.total += result.duration
                if result.success:
                    results.has_success = True
                else:
                    results.has_errors = True
                self._after_each(self, test, i)
                if self.debug and not result.success:
                    results.error = result.result
                    break
            self.after()
            self._after(self, test)

        self.after_class()
