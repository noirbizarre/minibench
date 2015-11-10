Console Client
==============

MiniBench comes with a console client `bench`.

This client takes a list of glob patterns as parameters.
If none is provided, it default on ``**/*.bench.py``.

.. code-block:: console

    $ bench
    $ bench benchmarks/*.bench.py
    $ bench benchs/*.bench tests/*.bench


Override Times
--------------

You can overrides how many ``times`` a methods are called with the ``--times`` option

.. code-block:: console

    $ bench -t 10000
    $ bench --times 1000


Export reports
--------------

You can export the result summary to the following formats:

- JSON
- CSV
- reStructuredText
- Markdown

.. code-block:: console

    $ bench --json out.json --csv out.csv
    $ bench --rst out.rst --md out.md


Run against a reference
-----------------------

MiniBench provides an easy to compare results against a previous JSON report with the ``--ref`` option.

.. code-block:: console

    $ bench --json out.json -t 100
    Running 1 benchmark
    -------------------
    >>> Glob benchmark (x100)
    Fnmatch..................................... ✔ 1.61257s / 0.01613s
    Glob........................................ ✔ 2.02383s / 0.02024s
    Re.......................................... ✔ 1.39118s / 0.01391s
    ✔ Done

    $ bench --ref out.json -t 100
    Running 1 benchmark
    -------------------
    >>> Glob benchmark (x100)
    Fnmatch.............. ✔ 1.60748s (-0.00508s) / 0.01607s (-0.00005s)
    Glob................. ✔ 1.97594s (-0.04788s) / 0.01976s (-0.00048s)
    Re................... ✔ 1.48161s (+0.09043s) / 0.01482s (+0.00090s)
    ✔ Done

Bash completion
---------------

A bash completion script is provided in the minibench github repository: `bench-completion.sh`_.

.. _bench-completion.sh: https://raw.githubusercontent.com/noirbizarre/minibench/master/bash-completion.sh
