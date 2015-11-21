Contributing
============

MiniBench is open-source and very open to contributions.

Submitting issues
-----------------

Issues are contributions in a way so don't hesitate
to submit reports on the `official bugtracker`_.

Provide as much informations as possible to specify the issues:

- the minibench version
- a stacktrace
- installed applications list
- a code sample to reproduce the issue
- ...


Submitting patches (bugfix, features, ...)
------------------------------------------

If you want to contribute some code:

1. fork the `official minibench repository`_
2. create a branch with an explicit name (like ``my-new-feature`` or ``issue-XX``)
3. do your work in it
4. rebase it on the master branch from the official repository (cleanup your history by performing an interactive rebase)
5. submit your pull-request

There are some rules to follow:

- your contribution should be documented (if needed)
- your contribution should be tested and the test suite should pass successfully
- your code should be mostly PEP8 compatible with a 120 characters line length
- your contribution should support both Python 2 and 3 (use ``tox`` to test)

You need to install some dependencies to develop on minibench:

.. code-block:: console

    $ pip install -e .[test,dev]

An Invoke ``tasks.py`` is provided to simplify the common tasks:

.. code-block:: console

    $ inv -l
    Available tasks:

      all          Run tests, reports and packaging
      clean        Cleanup all build artifacts
      completion   Generate bash completion script
      cover        Run tests suite with coverage
      dist         Package for distribution
      doc          Build the documentation
      qa           Run a quality report
      test         Run tests suite
      tox          Run test in all Python versions


To ensure everything is fine before submission, use ``tox``.
It will run the test suite on all the supported Python version
and ensure the documentation is generating.

.. code-block:: console

    $ tox

You also need to ensure your code is compliant with the minibench coding standards:

.. code-block:: console

    $ inv qa


.. _official minibench repository: https://github.com/noirbizarre/minibench
.. _official bugtracker: https://github.com/noirbizarre/minibench/issues
