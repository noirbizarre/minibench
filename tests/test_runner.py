# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import six
import unittest

from minibench import Benchmark, BaseReporter, BenchmarkRunner

from . import EXAMPLES


class CountReporter(BaseReporter):
    def __init__(self, **kwargs):
        self.counts = {
            'start': 0,
            'before_class': 0,
            'after_class': 0,
            'before_method': 0,
            'after_method': 0,
            'progress': 0,
            'end': 0,
        }

    def start(self):
        self.counts['start'] += 1

    def before_class(self, bench):
        assert isinstance(bench, Benchmark)
        self.counts['before_class'] += 1

    def after_class(self, bench):
        assert isinstance(bench, Benchmark)
        self.counts['after_class'] += 1

    def before_method(self, bench, method):
        assert isinstance(bench, Benchmark)
        assert isinstance(method, six.string_types)
        self.counts['before_method'] += 1

    def after_method(self, bench, method):
        assert isinstance(bench, Benchmark)
        assert isinstance(method, six.string_types)
        self.counts['after_method'] += 1

    def progress(self, bench, method, times):
        assert isinstance(bench, Benchmark)
        assert isinstance(method, six.string_types)
        assert times >= 0
        self.counts['progress'] += 1

    def end(self):
        self.counts['end'] += 1


class RunnerTests(unittest.TestCase):
    def test_load_module(self):
        filename = os.path.join(EXAMPLES, 'sort.bench.py')
        runner = BenchmarkRunner()

        module = runner.load_module(filename)

        self.assertEqual(module.__name__, 'benchmarks.sort')
        self.assertTrue(hasattr(module, 'SortDictByValue'))

    def test_should_load_benches_from_modules(self):
        filename = os.path.join(EXAMPLES, 'sort.bench.py')
        expected = ('SortDictByValue', 'SortLargerDictByValue')

        runner = BenchmarkRunner(filename)

        self.assertEqual(len(runner.benchmarks), 2)
        names = [b.__name__ for b in runner.benchmarks]
        for bench in expected:
            self.assertIn(bench, names)

    def test_store_runned_benchmark_instances(self):
        filename = os.path.join(EXAMPLES, 'empty.bench.py')

        runner = BenchmarkRunner(filename)
        runner.run()

        self.assertEqual(len(runner.runned), 1)
        self.assertIsInstance(runner.runned[0], Benchmark)

    def test_benchmark_in_debug(self):
        filename = os.path.join(EXAMPLES, 'fail.bench.py')

        runner = BenchmarkRunner(filename, debug=True)
        runner.run()

        self.assertEqual(len(runner.runned), 1)
        self.assertIsInstance(runner.runned[0], Benchmark)

        bench = runner.runned[0]
        self.assertTrue(bench.debug)

    def test_hook_reporter(self):
        filename = os.path.join(EXAMPLES, 'empty.bench.py')
        reporter = CountReporter()

        runner = BenchmarkRunner(filename, reporters=[reporter])
        self.assertEqual(len(runner.reporters), 1)
        self.assertEqual(runner.reporters[0], reporter)

        runner.run()

        self.assertEqual(reporter.counts, {
            'start': 1,
            'before_class': 1,
            'after_class': 1,
            'before_method': 1,
            'after_method': 1,
            'progress': 5,
            'end': 1,
        })

    def test_unsupported_reporter_is_ignored(self):
        class BadReporter(object):
            pass
        runner = BenchmarkRunner(reporters=[BadReporter])

        self.assertEqual(len(runner.reporters), 0)
