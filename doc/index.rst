.. MiniBench documentation master file, created by
   sphinx-quickstart on Wed Oct 28 14:23:04 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to MiniBench's documentation!
=====================================

MiniBench provides a simple framework for benchmarking following the ``unittest`` module pattern.

You can install minibench with pip:

.. code-block:: console

    $ pip install minibench


Then, you just have to write a ``.bench.py`` file.

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

Contents:

.. toctree::
   :maxdepth: 2

   quickstart
   benchmark
   client
   reporters
   api
   changelog



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
