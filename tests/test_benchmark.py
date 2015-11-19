# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time
import unittest

from minibench import Benchmark, DEFAULT_TIMES
from minibench.utils import humanize


class CountHooks(Benchmark):

    def __init__(self, *args, **kwargs):
        super(CountHooks, self).__init__(*args, **kwargs)
        self.runs = {
            'before_class': 0,
            'before': 0,
            'before_each': 0,
            'after_class': 0,
            'after': 0,
            'after_each': 0
        }


class BenchmarkTest(unittest.TestCase):

    def test_defaults(self):
        bench = Benchmark()
        self.assertEqual(bench.times, DEFAULT_TIMES)

    def test_times_constructor(self):
        bench = Benchmark(times=10)
        self.assertEqual(bench.times, 10)

    def test_times_attribute(self):
        class Test(Benchmark):
            times = 42
        bench = Test()
        self.assertEqual(bench.times, 42)

    def test_default_label(self):
        class Test(Benchmark):
            pass

        bench = Test()
        self.assertEqual(bench.label, humanize('Test'))

    def test_docstring_label(self):
        class Test(Benchmark):
            '''
            A simple test benchmark.
            This should be striped
            '''
            pass

        bench = Test()
        self.assertEqual(bench.label, 'A simple test benchmark.')

    def test_default_label_for(self):
        class Test(Benchmark):
            def bench_something(self):
                pass

        bench = Test()
        self.assertEqual(bench.label_for('bench_something'), humanize('something'))

    def test_docstring_label_for(self):
        class Test(Benchmark):
            def bench_something(self):
                '''
                A simple test benchmark.
                This should be striped
                '''
                pass

        bench = Test()
        self.assertEqual(bench.label_for('bench_something'), 'A simple test benchmark.')

    def test_collect_default(self):

        class Test(Benchmark):

            def bench_found(self):
                pass

            def bench_found_2(self):
                pass

            def not_found(self):
                pass

        bench = Test()
        self.assertEqual(bench._collect(), ['bench_found', 'bench_found_2'])

    def test_collect_custom_prefix(self):

        class Test(Benchmark):

            def test_found(self):
                pass

            def test_found_2(self):
                pass

            def bench_not_found(self):
                pass

            def not_found(self):
                pass

        bench = Test(prefix='test_')
        self.assertEqual(bench._collect(), ['test_found', 'test_found_2'])

    def test_hooks(self):
        class CountAllHooks(CountHooks):

            def before_class(self):
                self.runs['before_class'] += 1

            def before(self):
                self.runs['before'] += 1

            def before_each(self):
                self.runs['before_each'] += 1

            def after_class(self):
                self.runs['after_class'] += 1

            def after(self):
                self.runs['after'] += 1

            def after_each(self):
                self.runs['after_each'] += 1

            def bench_hook(self):
                pass

        class CountAllHooks2(CountAllHooks):

            def bench_hook_2(self):
                pass

        bench = CountHooks()
        bench.run()
        self.assertEqual(bench.runs, {
            'before_class': 0,
            'before': 0,
            'before_each': 0,
            'after_class': 0,
            'after': 0,
            'after_each': 0
        })

        bench = CountAllHooks()
        bench.run()
        self.assertEqual(bench.runs, {
            'before_class': 1,
            'before': 1,
            'before_each': 5,
            'after_class': 1,
            'after': 1,
            'after_each': 5
        })

        bench = CountAllHooks2()
        bench.run()
        self.assertEqual(bench.runs, {
            'before_class': 1,
            'before': 2,
            'before_each': 10,
            'after_class': 1,
            'after': 2,
            'after_each': 10
        })

    def test_constructor_hooks(self):
        def before(bench, method):
            bench.runs['before'] += 1

        def before_each(bench, method, iteration):
            bench.runs['before_each'] += 1

        def after(bench, method):
            bench.runs['after'] += 1

        def after_each(bench, method, iteration):
            bench.runs['after_each'] += 1

        class CountAllHooks(CountHooks):

            def bench_hook(self):
                pass

        class CountAllHooks2(CountAllHooks):

            def bench_hook_2(self):
                pass

        def assert_counts(cls, counts):
            bench = cls(times=5,
                        before=before,
                        before_each=before_each,
                        after=after,
                        after_each=after_each)
            bench.run()
            self.assertEqual(bench.runs, counts)

        assert_counts(CountHooks, {
            'before_class': 0,
            'before': 0,
            'before_each': 0,
            'after_class': 0,
            'after': 0,
            'after_each': 0
        })

        assert_counts(CountAllHooks, {
            'before_class': 0,
            'before': 1,
            'before_each': 5,
            'after_class': 0,
            'after': 1,
            'after_each': 5
        })

        assert_counts(CountAllHooks2, {
            'before_class': 0,
            'before': 2,
            'before_each': 10,
            'after_class': 0,
            'after': 2,
            'after_each': 10
        })

    def test_results(self):

        class SleepBench(Benchmark):

            def bench_results(self):
                time.sleep(0.1)

        bench = SleepBench(times=3)
        bench.run()

        result = bench.results['bench_results']
        self.assertGreaterEqual(result.total, bench.times * 0.1)
        self.assertTrue(result.has_success)
        self.assertFalse(result.has_errors)

    def test_failure(self):

        class FailBench(Benchmark):

            def bench_failure(self):
                raise Exception()

        bench = FailBench(times=3)
        bench.run()

        result = bench.results['bench_failure']
        self.assertGreater(result.total, 0)
        self.assertFalse(result.has_success)
        self.assertTrue(result.has_errors)

    def test_stop_on_failure_in_debug(self):
        def before_each(bench, method, iteration):
            assert iteration <= 1, 'Should stop on first error'

        class FailBench(Benchmark):

            def bench_failure(self):
                raise ValueError('Failed')

        bench = FailBench(times=3, debug=True, before_each=before_each)
        bench.run()

        result = bench.results['bench_failure']
        self.assertGreater(result.total, 0)
        self.assertFalse(result.has_success)
        self.assertTrue(result.has_errors)
        self.assertIsInstance(result.error, ValueError)
