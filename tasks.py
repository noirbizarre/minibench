# -*- coding: utf-8 -*-
# flake8: noqa
from __future__ import unicode_literals, absolute_import

from invoke import run, task

from os.path import join, abspath, dirname

ROOT = abspath(join(dirname(__file__)))


def lrun(cmd, **kwargs):
    return run('cd {root} && {cmd}'.format(root=ROOT, cmd=cmd), **kwargs)


@task
def clean(docs=False, bytecode=False, extra=''):
    '''Cleanup all build artifacts'''
    patterns = ['build', 'dist', 'cover', 'docs/_build', '**/*.pyc', '*.egg-info', '.tox', '**/__pycache__']
    for pattern in patterns:
        print('Removing {0}'.format(pattern))
        lrun('rm -rf {0}'.format(pattern))


@task
def test():
    '''Run tests suite'''
    lrun('nosetests --rednose --force-color', pty=True)


@task
def cover():
    '''Run tests suite with coverage'''
    lrun('nosetests --rednose --force-color --with-coverage '
         '--cover-html --cover-package=minibench', pty=True)


@task
def tox():
    '''Run test in all Python versions'''
    lrun('tox', pty=True)


@task
def qa():
    '''Run a quality report'''
    lrun('flake8 minibench')


@task
def doc():
    '''Build the documentation'''
    lrun('cd doc && make html', pty=True)


@task
def completion():
    '''Generate bash completion script'''
    lrun('_BENCH_COMPLETE=source bench > bench-complete.sh', pty=True)


@task
def dist():
    '''Package for distribution'''
    lrun('python setup.py sdist bdist_wheel', pty=True)


@task(clean, tox, doc, qa, dist, default=True)
def all():
    '''Run tests, reports and packaging'''
    pass
