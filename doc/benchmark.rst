Writing benchmarks
==================

Basics
------

Writing a benchmark is as simple as extenting :class:`~minibench.Benchmark`.
Each method will be run :attr:`~minibench.Benchmark.times` times.
A benchmark method should start with ``bench_``.

.. code-block:: python

    from minibench import Benchmark


    class SumBenchmark(Benchmark):
        times = 1000

        def bench_sum(self):
            sum(x for x in range(5))

        def bench_consecutive_add(self):
            total = 0
            for x in range(5):
                total += x

.. code-block:: console

    $ bench examples/sum.bench.py
    Running 1 benchmark
    -------------------
    >>> Sum benchmark (x1000)
    Consecutive add................... ✔ 0.00142s / 0.00000s
    Sum............................... ✔ 0.00245s / 0.00000s
    ✔ Done


Documenting
-------------

Documenting you benchmark is as simple as writing explicit docstrings.
Only the first line will be kept.

.. code-block:: python

    from minibench import Benchmark


    class SumBenchmark(Benchmark):
        '''
        A simple sum benchmark

        This will be ignored.
        '''
        times = 1000

        def bench_sum(self):
            '''Sum using sum()'''
            sum(x for x in range(5))

        def bench_consecutive_add(self):
            '''Sum using +='''
            total = 0
            for x in range(5):
                total += x


.. code-block:: console

    $ bench examples/sum.bench.py
    Running 1 benchmark
    -------------------
    >>> A simple sum benchmark (x1000)
    Sum using sum()............................ ✔ 0.00142s / 0.00000s
    Sum using +=............................... ✔ 0.00245s / 0.00000s
    ✔ Done


Hooks
-----

The :class:`~minibench.Benchmark` provide some hooks as methods:

- :meth:`~minibench.Benchmark.before_class`: executed once before each class
- :meth:`~minibench.Benchmark.before`: executed once before each method
- :meth:`~minibench.Benchmark.before_each`: executed before each method call
- :meth:`~minibench.Benchmark.after_class`: executed once after each class
- :meth:`~minibench.Benchmark.after`: executed once after each method
- :meth:`~minibench.Benchmark.after_each`: executed after each method call

.. code-block:: python

    from minibench import Benchmark

    class MyBench(Benchmark):

        def before_class(self):
            # Will be executed once before all class methods
            pass

        def before(self):
            # Will be executed once before each method
            pass

        def before_each(self):
            # Will be executed before each method call
            pass

        def after_class(self):
            # Will be executed once after all class methods
            pass

        def after(self):
            # Will be executed once after each method
            pass

        def after_each(self):
            # Will be executed aftereach method call
            pass
