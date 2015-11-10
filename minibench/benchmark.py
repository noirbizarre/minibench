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


class Benchmark(object):
    '''Base class for all benchmark suites'''
    times = DEFAULT_TIMES

    def __init__(self, times=None, prefix="bench_",
                 before=None, before_each=None,
                 after=None, after_each=None,
                 **kwargs):

        self.times = times or self.times
        self.results = {}

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
        result = func()
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
            results = self.results[test] = []
            self._before(self, test)
            self.before()
            for i in range(self.times):
                self._before_each(self, test, i)
                results.append(self._run_one(func))
                self._after_each(self, test, i)
            self.after()
            self._after(self, test)

        self.after_class()
