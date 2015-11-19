# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import inspect
import logging
import os


from . import Benchmark
from .report import BaseReporter
from ._compat import load_module, string_types

log = logging.getLogger(__name__)


class BenchmarkRunner(object):
    '''Collect all benchmarks and run them'''
    def __init__(self, *filenames, **kwargs):
        '''
        :param filenames: the benchmark files names
        :type filenames: string
        :param reporters: the reporters classes or instance to run
        :type reporters: list
        :param debug: Run in debug mode if ``True``
        :type debug: bool
        '''
        self.benchmarks = []
        self.runned = []
        self.reporters = []
        self.debug = kwargs.get('debug', False)

        for filename in filenames:
            module = self.load_module(filename)
            benchmarks = self.load_from_module(module)
            self.benchmarks.extend(benchmarks)

        for reporter in kwargs.get('reporters', []):
            if inspect.isclass(reporter) and issubclass(reporter, BaseReporter):
                reporter = reporter()
            if isinstance(reporter, BaseReporter):
                reporter.init(self)
                self.reporters.append(reporter)
            else:
                log.warning('Unsupported reporter %s', reporter)

    def run(self, **kwargs):
        '''
        Run all benchmarks.

        Extras kwargs are passed to benchmarks construtors.
        '''
        self.report_start()
        for bench in self.benchmarks:
            bench = bench(before=self.report_before_method,
                      after=self.report_after_method,
                      after_each=self.report_progress,
                      debug=self.debug,
                      **kwargs)
            self.report_before_class(bench)
            bench.run()
            self.report_after_class(bench)
            self.runned.append(bench)
        self.report_end()

    def load_module(self, filename):
        '''Load a benchmark module from file'''
        if not isinstance(filename, string_types):
            return filename
        basename = os.path.splitext(os.path.basename(filename))[0]
        basename = basename.replace('.bench', '')
        modulename = 'benchmarks.{0}'.format(basename)
        return load_module(modulename, filename)

    def load_from_module(self, module):
        '''Load all benchmarks from a given module'''
        benchmarks = []
        for name in dir(module):
            obj = getattr(module, name)
            if (inspect.isclass(obj) and issubclass(obj, Benchmark)
                    and obj != Benchmark):
                benchmarks.append(obj)
        return benchmarks

    def report_start(self):
        for reporter in self.reporters:
            reporter.start()

    def report_before_class(self, bench):
        for reporter in self.reporters:
            reporter.before_class(bench)

    def report_after_class(self, bench):
        for reporter in self.reporters:
            reporter.after_class(bench)

    def report_before_method(self, bench, method):
        for reporter in self.reporters:
            reporter.before_method(bench, method)

    def report_after_method(self, bench, method):
        for reporter in self.reporters:
            reporter.after_method(bench, method)

    def report_progress(self, bench, method, times):
        for reporter in self.reporters:
            reporter.progress(bench, method, times)

    def report_end(self):
        for reporter in self.reporters:
            reporter.end()
