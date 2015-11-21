# -*- coding: utf-8 -*-
import json as JSON
import os

import click

from ._compat import recursive_glob
from .report import BaseReporter, JsonReporter, CsvReporter, MarkdownReporter, RstReporter, DEFAULT_PRECISION
from .runner import BenchmarkRunner


CONTEXT_SETTINGS = {
    'help_option_names': ['-?', '-h', '--help']
}


def color(name, **kwargs):
    return lambda t: click.style(str(t), fg=name, **kwargs)

green = color('green', bold=True)
yellow = color('yellow', bold=True)
red = color('red', bold=True)
cyan = color('cyan')
magenta = color('magenta', bold=True)
white = color('white', bold=True)


OK = '✔'
KO = '✘'
WARNING = '⚠'

UNIT_PERCENTS = ('%', 'percents')
UNIT_SECONDS = ('s', 'seconds')
DEFAULT_UNIT = '%'

FORMAT_DURATION = '{total:.{precision}f}s / {mean:.{precision}f}s'
FORMAT_DIFF = '{total:.{precision}f}s / {mean:.{precision}f}s ({diff})'


class CliReporter(BaseReporter):
    '''A reporter that display running benchmarks with ANSI colors'''
    def __init__(self, ref=None, debug=False, unit=DEFAULT_UNIT, **kwargs):
        self._ref = ref
        self.debug = debug
        self.is_percent = unit in UNIT_PERCENTS
        super(CliReporter, self).__init__(**kwargs)

    def start(self):
        nb_benchmarks = len(self.runner.benchmarks)
        if nb_benchmarks > 1:
            msg = 'Running {0} benchmarks'.format(nb_benchmarks)
        else:
            msg = 'Running {0} benchmark'.format(nb_benchmarks)
        click.echo(white(msg))
        click.echo(white('-' * len(msg)))

    def before_class(self, bench):
        label = '>>> {name} (x{times})'.format(name=bench.label,
                                               times=bench.times)
        click.echo(magenta(label))

    def after_class(self, bench):
        pass

    def before_method(self, bench, method):
        label = cyan(bench.label_for(method))
        self.bar = click.progressbar(label=label, length=bench.times)
        self.bar.render_progress()

    def after_method(self, bench, method):
        click.echo('\r', nl=False)  # Clear the line

        results = bench.results[method]
        mean = results.total / bench.times
        ref = self.ref(bench, method)
        duration = self.duration(total=results.total, mean=mean, ref=ref)

        if results.has_success and results.has_errors:
            status = ' '.join((yellow(WARNING), duration))
        elif results.has_success:
            status = ' '.join((green(OK), duration))
        else:
            status = ' '.join((red(KO), duration))

        width, _ = click.get_terminal_size()
        size = width - len(click.unstyle(status))

        label = bench.label_for(method)

        click.echo('{label:.<{size}} {status}'.format(label=cyan(label),
                                                      size=size,
                                                      status=status))
        if self.debug and results.error:
            exc = results.error
            click.echo(yellow('Error: {0}'.format(type(exc))))
            click.echo('\t{0}'.format(exc.message if hasattr(exc, 'message') else exc))

    def ref(self, bench, method):
        if self._ref:
            key = self.key(bench)
            return self._ref.get(key, {}).get('runs', {}).get(method, None)

    def duration(self, total, mean, ref=None):
        if ref:
            diff = self.diff(total, mean, ref)
            duration = FORMAT_DIFF.format(total=total, mean=mean,
                                          diff=diff, precision=self.precision)
        else:
            duration = FORMAT_DURATION.format(total=total, mean=mean, precision=self.precision)
        return duration

    def diff(self, total, mean, ref):
        diff = self._r(total) - self._r(ref['total'])
        if diff > 0:
            if self.is_percent:
                msg = '+{0:.2%}'.format(diff / self._r(ref['total']))
            else:
                mean_diff = self._r(mean) - self._r(ref['mean'])
                msg = '+{total:.{precision}f}s / +{mean:.{precision}f}s'
                msg = msg.format(total=diff, mean=mean_diff, precision=self.precision)
            return red(msg)
        elif diff < 0:
            if self.is_percent:
                msg = '{0:.2%}'.format(diff / self._r(ref['total']))
            else:
                mean_diff = self._r(mean) - self._r(ref['mean'])
                msg = '{total:.{precision}f}s / {mean:.{precision}f}s'
                msg = msg.format(total=diff, mean=mean_diff, precision=self.precision)
            return green(msg)
        else:
            return cyan('---')

    def _r(self, value):
        '''Round a value according defined precision'''
        return round(value, self.precision)

    def progress(self, bench, method, times):
        self.bar.update(times)

    def end(self):
        click.echo(green(' '.join((OK, 'Done'))))


def resolve_pattern(pattern):
    '''Resolve a glob pattern into a filelist'''
    if os.path.exists(pattern) and os.path.isdir(pattern):
        pattern = os.path.join(pattern, '**/*.bench.py')
    return recursive_glob(pattern)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('patterns', nargs=-1)
@click.option('-t', '--times', type=click.INT, help='How many times to run benchmarks')
@click.option('--json', type=click.Path(), help='Output results as JSON')
@click.option('--csv', type=click.Path(), help='Output results as CSV')
@click.option('--rst', type=click.Path(), help='Output results as reStructuredText')
@click.option('--md', type=click.Path(), help='Output results as Markdown')
@click.option('-r', '--ref', type=click.File('r'), help='A previous run result in JSON')
@click.option('-u', '--unit', default=DEFAULT_UNIT,
              type=click.Choice(UNIT_PERCENTS + UNIT_SECONDS),
              help='Unit to display difference from reference')
@click.option('-p', '--precision', type=click.INT, default=DEFAULT_PRECISION,
              help='Precision used (number of digits)')
@click.option('-d', '--debug', is_flag=True, help='Run in debug (verbose, stop on error)')
def cli(patterns, times, json, csv, rst, md, ref, unit, precision, debug):
    '''Execute minibench benchmarks'''
    if ref:
        ref = JSON.load(ref)

    filenames = []
    reporters = [CliReporter(ref=ref, debug=debug, unit=unit, precision=precision)]
    kwargs = {}
    for pattern in patterns or ['**/*.bench.py']:
        filenames.extend(resolve_pattern(pattern))
    if json:
        reporters.append(JsonReporter(json, precision=precision))
    if csv:
        reporters.append(CsvReporter(csv, precision=precision))
    if rst:
        reporters.append(RstReporter(rst, precision=precision))
    if md:
        reporters.append(MarkdownReporter(md, precision=precision))
    if times:
        kwargs['times'] = times
    runner = BenchmarkRunner(*filenames, reporters=reporters, debug=debug)
    runner.run(**kwargs)
