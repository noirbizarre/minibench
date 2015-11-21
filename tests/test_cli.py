# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest
import os

from click.testing import CliRunner

from minibench.cli import resolve_pattern, cli

from . import EXAMPLES


class ClientTest(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()

    def assertMatch(self, resolved, expected):
        self.assertEqual(len(resolved), len(expected))
        for filename in expected:
            self.assertIn(filename, resolved)

    def test_single_sibling_file(self):
        with self.runner.isolated_filesystem():
            with open('test.bench.py', 'w') as f:
                f.write('')

            resolved = resolve_pattern('test.bench.py')

        self.assertEqual(resolved, ['test.bench.py'])

    def test_single_nested_file(self):
        with self.runner.isolated_filesystem():
            os.mkdir('nested')
            with open('nested/test.bench.py', 'w') as f:
                f.write('')

            resolved = resolve_pattern('nested/test.bench.py')

        self.assertEqual(resolved, ['nested/test.bench.py'])

    def test_glob_single_sibling_file(self):
        with self.runner.isolated_filesystem():
            with open('test.bench.py', 'w') as f:
                f.write('')

            resolved = resolve_pattern('*')

        self.assertEqual(resolved, ['test.bench.py'])

    def test_glob_single_nested_file(self):
        with self.runner.isolated_filesystem():
            os.mkdir('nested')
            with open('nested/test.bench.py', 'w') as f:
                f.write('')

            resolved = resolve_pattern('nested/*')

        self.assertEqual(resolved, ['nested/test.bench.py'])

    def test_glob_cwd(self):
        with self.runner.isolated_filesystem():
            with open('test1.bench.py', 'w') as f:
                f.write('')
            with open('test2.bench.py', 'w') as f:
                f.write('')

            resolved = resolve_pattern('*')

        self.assertMatch(resolved, ['test1.bench.py', 'test2.bench.py'])

    def test_glob_directory(self):
        with self.runner.isolated_filesystem():
            os.mkdir('nested')
            with open('nested/test1.bench.py', 'w') as f:
                f.write('')
            with open('nested/test2.bench.py', 'w') as f:
                f.write('')

            resolved = resolve_pattern('nested/*')

        self.assertMatch(resolved, ['nested/test1.bench.py',
                                    'nested/test2.bench.py'])

    def test_findall_cwd(self):
        with self.runner.isolated_filesystem():
            os.mkdir('nested')
            with open('nested/test1.bench.py', 'w') as f:
                f.write('')
            with open('nested/test2.bench.py', 'w') as f:
                f.write('')
            os.mkdir('nested2')
            with open('nested2/test1.bench.py', 'w') as f:
                f.write('')
            with open('nested2/test2.bench.py', 'w') as f:
                f.write('')

            resolved = resolve_pattern('.')

        expected = ['./nested/test1.bench.py', './nested/test2.bench.py',
                    './nested2/test1.bench.py', './nested2/test2.bench.py']

        self.assertMatch(resolved, expected)

    def test_findall_directory(self):
        with self.runner.isolated_filesystem():
            os.mkdir('nested')
            with open('nested/test1.bench.py', 'w') as f:
                f.write('')
            with open('nested/test2.bench.py', 'w') as f:
                f.write('')
            os.mkdir('nested/nested2')
            with open('nested/nested2/test1.bench.py', 'w') as f:
                f.write('')
            with open('nested/nested2/test2.bench.py', 'w') as f:
                f.write('')

            resolved = resolve_pattern('nested/')

        expected = ['nested/test1.bench.py', 'nested/test2.bench.py',
                    'nested/nested2/test1.bench.py',
                    'nested/nested2/test2.bench.py']

        self.assertMatch(resolved, expected)

    def test_cli_without_benchmarks(self):
        result = self.runner.invoke(cli, ['-h'])
        self.assertEqual(result.exit_code, 0)

    def test_cli_on_benchmark(self):
        filename = os.path.join(EXAMPLES, 'empty.bench.py')
        result = self.runner.invoke(cli, [filename])
        self.assertEqual(result.exit_code, 0, result.exception)

    def test_cli_with_json_report(self):
        filename = os.path.join(EXAMPLES, 'empty.bench.py')
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, [filename, '--json', 'out.json'])
            self.assertEqual(result.exit_code, 0, result.exception)
            self.assertTrue(os.path.exists('out.json'), 'Should output report as JSON')

    def test_cli_with_csv_report(self):
        filename = os.path.join(EXAMPLES, 'empty.bench.py')
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, [filename, '--csv', 'out.csv'])
            self.assertEqual(result.exit_code, 0, result.exception)
            self.assertTrue(os.path.exists('out.csv'), 'Should output report as CSV')

    def test_cli_with_rst_report(self):
        filename = os.path.join(EXAMPLES, 'empty.bench.py')
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, [filename, '--rst', 'out.rst'])
            self.assertEqual(result.exit_code, 0, result.exception)
            self.assertTrue(os.path.exists('out.rst'), 'Should output report as reStructerdText')

    def test_cli_with_markdown_report(self):
        filename = os.path.join(EXAMPLES, 'empty.bench.py')
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, [filename, '--md', 'out.md'])
            self.assertEqual(result.exit_code, 0, result.exception)
            self.assertTrue(os.path.exists('out.md'), 'Should output report as Markdown')

    def test_cli_with_debug(self):
        filename = os.path.join(EXAMPLES, 'fail.bench.py')
        result = self.runner.invoke(cli, ['-d', filename])
        self.assertIn('I failed', result.output)

    def test_cli_with_ref(self):
        filename = os.path.join(EXAMPLES, 'empty.bench.py')
        with self.runner.isolated_filesystem():
            self.runner.invoke(cli, [filename, '--json', 'ref.json'])
            result = self.runner.invoke(cli, [filename, '--ref', 'ref.json'])
            self.assertEqual(result.exit_code, 0, result.exception)

    def test_cli_with_ref_unit_seconds(self):
        filename = os.path.join(EXAMPLES, 'empty.bench.py')
        with self.runner.isolated_filesystem():
            self.runner.invoke(cli, [filename, '--json', 'ref.json'])
            result = self.runner.invoke(cli, [filename, '--ref', 'ref.json', '-u', 'seconds'])
            self.assertEqual(result.exit_code, 0, result.exception)
