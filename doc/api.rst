API
===

.. module:: minibench

This part of the documentation lists the full API reference of all public
classes and functions.

Core
----

    .. autoclass:: Benchmark
        :members:

        .. autoattribute:: times
            :annotation: = The number of iteration to run each method

    .. autoclass:: RunResult

    .. autoclass:: BenchmarkRunner
        :members:


Reporters
---------

.. autoclass:: BaseReporter
    :members:

.. autoclass:: FileReporter
    :members:

.. autoclass:: JsonReporter
    :members:

.. autoclass:: CsvReporter
    :members:

.. autoclass:: MarkdownReporter
    :members:

.. autoclass:: RstReporter
    :members:


.. currentmodule:: minibench.cli

.. autoclass:: CliReporter
