=========
MiniBench
=========

.. image:: https://secure.travis-ci.org/noirbizarre/minibench.png
    :target: http://travis-ci.org/noirbizarre/minibench
    :alt: Build status
.. image:: https://coveralls.io/repos/noirbizarre/minibench/badge.png?branch=0.1.0
    :target: https://coveralls.io/r/noirbizarre/minibench?branch=0.1.0
    :alt: Code coverage
.. image:: https://requires.io/github/noirbizarre/minibench/requirements.png?tag=0.1.0
    :target: https://requires.io/github/noirbizarre/minibench/requirements/?tag=0.1.0
    :alt: Requirements Status
.. image:: https://readthedocs.org/projects/minibench/badge/?version=0.1.0
    :target: http://minibench.readthedocs.org/en/0.1.0/
    :alt: Documentation status

MiniBench provides a simple framework for benchmarking following the ``unittest`` module pattern.

Compatibility
=============

minibench requires Python 2.7+.


Installation
============

You can install minibench with pip:

.. code-block:: console

    $ pip install minibench

or with easy_install:

.. code-block:: console

    $ easy_install minibench


Quick start
===========

Write your benchmarks as you would write you unittests.
Just create a ``.bench.py`` file.

.. code-block:: python

    # fake.bench.py
    from minibench import Benchmark

    class FakeBenchmark(Benchmark):
        '''Fake benchmark'''
        def bench_fake(self):
            '''Run my bench'''
            # Do something

Then run it with the ``bench`` command

.. code-block:: console

    $ bench
    >>> Fake benchmark (x5)
    Run my bench ......................................... ✔ (0.1234s)


Documentation
=============

The documentation is hosted `on Read the Docs <http://minibench.readthedocs.org/en/0.1.0/>`_
