# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv
import json
import os
import six
import unittest

from tempfile import NamedTemporaryFile
from xml.etree import ElementTree as ET

from docutils.core import publish_string
from markdown import markdown

from minibench import (
    BaseReporter,
    Benchmark,
    BenchmarkRunner,
    CsvReporter,
    FixedWidth,
    JsonReporter,
    MarkdownReporter,
    RstReporter,
)

from . import EXAMPLES, ModuleFactory


class BaseReporterTests(unittest.TestCase):
    def test_summary_without_docstrings(self):
        filename = os.path.join(EXAMPLES, 'empty.bench.py')
        reporter = BaseReporter()
        runner = BenchmarkRunner(filename, reporters=[reporter])
        runner.run()

        summary = reporter.summary()
        self.assertEqual(len(summary), 1)

        bench = runner.runned[0]
        key = reporter.key(bench)
        self.assertIn(key, summary)

        bench_summary = summary[key]
        self.assertEqual(bench_summary['name'], 'Empty benchmark')
        self.assertEqual(bench_summary['times'], 5)
        self.assertEqual(len(bench_summary['runs']), 1)

        row = bench_summary['runs']['bench_nothing']
        self.assertEqual(row['name'], 'Nothing')
        self.assertIn('total', row)
        self.assertIn('mean', row)


class JsonReporterTest(unittest.TestCase):
    def test_output_summary_as_json(self):
        filename = os.path.join(EXAMPLES, 'empty.bench.py')
        with NamedTemporaryFile() as out:
            reporter = JsonReporter(out.name)
            runner = BenchmarkRunner(filename, reporters=[reporter])
            runner.run()
            out.flush()
            data = json.loads(out.read().decode('utf8'))

        self.assertEqual(data, reporter.summary())


class CsvReporterTest(unittest.TestCase):
    def test_output_summary_as_json(self):
        filename = os.path.join(EXAMPLES, 'empty.bench.py')
        with NamedTemporaryFile() as out:
            reporter = CsvReporter(out.name)
            runner = BenchmarkRunner(filename, reporters=[reporter])
            runner.run()
            out.flush()
            with open(out.name) as csvfile:
                reader = csv.reader(csvfile, delimiter=str(';'), quotechar=str('"'))
                self.assertEqual(six.next(reader), ['Benchmark', 'Method', 'Times', 'Total (s)', 'Average (s)'])


class FixedWidthMixinText(unittest.TestCase):
    def test_summary_with_sizes(self):
        class TestReporter(BaseReporter, FixedWidth):
            pass

        class TestBench(Benchmark):
            def bench_short(self):
                pass

            def bench_long(self):
                '''A method with long label'''
                pass

        reporter = TestReporter()
        module = ModuleFactory(TestBench)
        runner = BenchmarkRunner(module, reporters=[reporter])
        runner.run()

        bench = runner.runned[0]
        key = reporter.key(bench)

        summary = reporter.with_sizes('', 'Method', 'Times', 'Total (s)', 'Average (s)')
        self.assertEqual(len(summary), 1)
        self.assertEqual(summary[key]['sizes'][1], len('A method with long label'))
        self.assertEqual(summary[key]['sizes'][2], len('Times'))

    def test_one_row_by_benchmark(self):
        class TestReporter(BaseReporter, FixedWidth):
            pass

        class TestBench(Benchmark):
            def bench_short(self):
                pass

        class AnotherBench(Benchmark):
            def bench_short(self):
                pass

        reporter = TestReporter()
        module = ModuleFactory(TestBench, AnotherBench)
        runner = BenchmarkRunner(module, reporters=[reporter])
        runner.run()

        summary = reporter.with_sizes('', 'Method', 'Times', 'Total (s)', 'Average (s)')
        self.assertEqual(len(summary), 2)

    def test_number_of_headers(self):
        class TestReporter(BaseReporter, FixedWidth):
            pass

        reporter = TestReporter()
        runner = BenchmarkRunner(reporters=[reporter])
        runner.run()

        with self.assertRaises(ValueError):
            reporter.with_sizes('One', 'Header', 'Is', 'Missing')


class RstReporterTest(unittest.TestCase):
    NAMESPACES = {'h': 'http://www.w3.org/1999/xhtml'}

    def findall(self, html, xpath):
        return html.findall(xpath, namespaces=self.NAMESPACES)

    def test_output_summary_as_restructuredtext(self):
        filename = os.path.join(EXAMPLES, 'empty.bench.py')
        with NamedTemporaryFile() as out:
            reporter = RstReporter(out.name)
            runner = BenchmarkRunner(filename, reporters=[reporter])
            runner.run()
            out.flush()

            rst = out.read()
            html = publish_string(rst, writer_name='html')
            tree = ET.fromstring(html)

            titles = self.findall(tree, './/h:h1')
            self.assertEqual(len(titles), 1)
            self.assertEqual(titles[0].text, 'Empty benchmark')

            tables = self.findall(tree, './/h:table')
            self.assertEqual(len(tables), 1)
            columns = self.findall(tables[0], './/h:th')
            self.assertEqual(len(columns), 4)


class MarkdownReporterTest(unittest.TestCase):
    def test_output_summary_as_markdown(self):
        filename = os.path.join(EXAMPLES, 'empty.bench.py')
        with NamedTemporaryFile() as out:
            reporter = MarkdownReporter(out.name)
            runner = BenchmarkRunner(filename, reporters=[reporter])
            runner.run()
            out.flush()

            md = out.read()
            html = markdown(md.decode('utf8'), extensions=['markdown.extensions.tables'])
            tree = ET.fromstring('<!DOCTYPE html><html><body>{0}</body></html>'.format(html))

            titles = tree.findall('.//h1')
            self.assertEqual(len(titles), 1)
            self.assertEqual(titles[0].text, 'Empty benchmark')

            tables = tree.findall('.//table')
            self.assertEqual(len(tables), 1)
            columns = tables[0].findall('.//th')
            self.assertEqual(len(columns), 4)
