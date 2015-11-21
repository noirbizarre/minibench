# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv
import json
import os

DEFAULT_PRECISION = 5


class BaseReporter(object):
    '''Base class for all reporters'''
    def __init__(self, precision=DEFAULT_PRECISION, **kwargs):
        self.precision = precision

    def init(self, runner):
        self.runner = runner

    def start(self):
        '''Hook called once on run start'''
        pass

    def before_class(self, bench):
        '''Hook called once before each benchmark class'''
        pass

    def after_class(self, bench):
        '''Hook called once after each benchmark class'''
        pass

    def before_method(self, bench, method):
        '''Hook called once before each benchmark method'''
        pass

    def after_method(self, bench, method):
        '''Hook called once after each benchmark method'''
        pass

    def progress(self, bench, method, times):
        '''Hook called after each benchmark method call'''
        pass

    def end(self):
        '''Hook called once on run end'''
        pass

    def summary(self):
        '''Compute the execution summary'''
        out = {}
        for bench in self.runner.runned:
            key = self.key(bench)
            runs = {}
            for method, results in bench.results.items():
                mean = results.total / bench.times
                name = bench.label_for(method)
                runs[method] = {
                    'name': name,
                    'total': results.total,
                    'mean': mean
                }
            out[key] = {
                'name': bench.label,
                'times': bench.times,
                'runs': runs
            }
        return out

    def key(self, bench):
        '''Generate a report key from a benchmark instance'''
        return '{bench.__class__.__name__}-{bench.times}'.format(bench=bench)


class FileReporter(BaseReporter):
    '''A reporter dumping results into a file'''
    def __init__(self, filename, **kwargs):
        '''
        :param filename: the output file name
        :type filename: string
        '''
        self.filename = filename
        super(FileReporter, self).__init__(**kwargs)

    def end(self):
        '''
        Dump the report into the output file.

        If the file directory does not exists, it will be created.
        The open file is then given as parameter to :meth:`~minibench.report.FileReporter.output`.
        '''
        dirname = os.path.dirname(self.filename)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(self.filename, 'w') as out:
            self.out = out
            self.output(out)
            self.out = None

    def output(self, out):
        '''
        Serialize the report into the open file.

        Child classes should implement this method.

        :param out: an open file object to serialize into.
        :type out: file
        '''
        raise NotImplementedError('You need to implement the output method')

    def line(self, text=''):
        '''A simple helper to write line with `\n`'''
        self.out.write(text)
        self.out.write('\n')


class JsonReporter(FileReporter):
    '''A reporter dumping results into a JSON file'''
    def output(self, out):
        json.dump(self.summary(), out)


class CsvReporter(FileReporter):
    '''
    A reporter dumping results into a CSV file

    The CSV will have the following format:

    =========  ======  =====  =========  ===========
    Benchmark  Method  Times  Total (s)  Average (s)
    =========  ======  =====  =========  ===========

    It uses `;` character as delimiter and `"` as delimiter.
    All Strings are quoted.
    '''
    def output(self, out):
        writer = csv.writer(out, delimiter=str(';'), quotechar=str('"'), quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(('Benchmark', 'Method', 'Times', 'Total (s)', 'Average (s)',))
        for row in self.summary().values():
            for run in row['runs'].values():
                writer.writerow((
                    row['name'],
                    run['name'],
                    row['times'],
                    run['total'],
                    run['mean'],
                ))


class FixedWidth(object):
    '''A mixins with helpers for fixed width tables raporters'''
    headers = ('Method', 'Times', 'Total (s)', 'Average (s)')

    def with_sizes(self, *headers):
        '''Compute the report summary and add the computed column sizes'''
        if len(headers) != 5:
            raise ValueError('You need to provide this headers: class, method, times, total, average')

        summary = self.summary()

        for row in summary.values():
            sizes = [len(header) for header in headers]
            # Benchmark/Class column
            sizes[0] = max(sizes[0], len(row['name']))
            # Method column
            max_length = max(len(r['name']) for r in row['runs'].values())
            sizes[1] = max(sizes[1], max_length)
            # Times column
            sizes[2] = max(sizes[2], len(str(row['times'])))
            # Float columns
            for idx, field in [(3, 'total'), (4, 'mean')]:
                float_len = lambda r: len(self.float(r[field]))
                max_length = max(float_len(r) for r in row['runs'].values())
                sizes[idx] = max(sizes[idx], max_length)
            row['sizes'] = sizes

        return summary

    def float(self, value):
        return '{0:.{1}f}'.format(value, self.precision)


class MarkdownReporter(FileReporter, FixedWidth):
    '''
    A reporter rendering result as a markdown table.

    Each benchmark will be rendered as a table with the following format:

    ======  =====  =========  ===========
    Method  Times  Total (s)  Average (s)
    ======  =====  =========  ===========
    '''
    def output(self, out):
        for bench in self.with_sizes('', *self.headers).values():
            # Bench label as title
            self.line('# {0}'.format(bench['name']))
            self.line()
            # Table header
            sizes = bench['sizes'][1:]
            headers = [h.ljust(s) for h, s in zip(self.headers, sizes)]
            self.row(headers)
            separators = ['-' * size for size in sizes]
            self.row(separators, ':')

            # Table body
            for run in bench['runs'].values():
                values = (run['name'], bench['times'], self.float(run['total']), self.float(run['mean']))
                values = [str(v).ljust(s) for v, s in zip(values, sizes)]
                self.row(values)
            self.line()

    def row(self, values, char=' '):
            self.line('|{c}{r[0]}{c}|{c}{r[1]}{c}|{c}{r[2]}{c}|{c}{r[3]}{c}|'.format(r=values, c=char))


class RstReporter(FileReporter, FixedWidth):
    '''
    A reporter rendering result as a reStructuredText table

    Each benchmark will be rendered as a table with the following format:

    ======  =====  =========  ===========
    Method  Times  Total (s)  Average (s)
    ======  =====  =========  ===========
    '''
    row = '| {row[0]: <{sizes[0]}} | {row[1]: <{sizes[1]}} | {row[2]: <{sizes[2]}} | {row[3]: <{sizes[3]}} |'

    def output(self, out):
        for bench in self.with_sizes('', *self.headers).values():
            # Bench label as title
            self.line(bench['name'])
            self.line('=' * len(bench['name']))
            self.line()
            # Table header
            sizes = bench['sizes'][1:]
            self.line(self.separator(sizes))
            line = self.row.format(row=self.headers, sizes=sizes)
            self.line(line)
            self.line(self.separator(sizes, '='))
            # Table body
            for run in bench['runs'].values():
                row = (run['name'], bench['times'], self.float(run['total']), self.float(run['mean']))
                line = self.row.format(row=row, sizes=sizes)
                self.line(line)
            # Table footer
            self.line(self.separator(sizes))
            self.line()

    def separator(self, sizes, char='-'):
        line = '+'.join([char * (size + 2) for size in sizes])
        return ''.join(('+', line, '+'))
