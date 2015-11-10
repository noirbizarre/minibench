Quickstart
==========

You can install minibench with pip:

.. code-block:: console

    $ pip install minibench

Write your benchmarks as you would write you unittests.
Just create ``.bench.py`` file.

.. code-block:: python

    # fake.bench.py
    from minibench import Benchmark

    class FakeBenchmark(Benchmark):
        '''Fake benchmark'''
        def bench_fake(self):
            '''Run my bench'''
            # Do something

        def bench_another(self):
            '''Another bench'''
            # Do something

Then run it with the ``bench`` command

.. code-block:: console

    $ bench
    >>> Fake benchmark (x5)
    Run my bench ................................ ✔ (0.1234s / 0.1233s)
    Another bench ............................... ✔ (0.1234s / 0.1233s)
