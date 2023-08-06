========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - |
        | |coveralls| |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|



.. |coveralls| image:: https://coveralls.io/repos/DonRegan/x-goals/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/DonRegan/x-goals

.. |codecov| image:: https://codecov.io/github/DonRegan/x-goals/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/DonRegan/x-goals

.. |version| image:: https://img.shields.io/pypi/v/x-goals.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/x-goals

.. |commits-since| image:: https://img.shields.io/github/commits-since/DonRegan/x-goals/v0.0.2.svg
    :alt: Commits since latest release
    :target: https://github.com/DonRegan/x-goals/compare/v0.0.2...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/x-goals.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/x-goals

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/x-goals.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/x-goals

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/x-goals.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/x-goals


.. end-badges

X-Goals package. Generated with cookiercutter-pylibrary using the command line cookiecutter gh:ionelmc/cookiecutter-
pylibrary

This is V1 of X-Goals which is an alternative method to score a match.

XGoals uses the weighting approach of 0.15 (corners), 0.2 (shots on) and -0.1 (cards).

Cards increases by 1 for a player's first yellow card, and by 2.5 for a second yellow or a red (motivated by
sportingindex.com weightings). Currently corners and shots on are modelled using the normal distribution, with
95% of values lying in the range [0, 2 times the expected value]; this means the spread is set to be half the expected
value (this is motivated by historical behaviour for teams over a whole season, and clearly that's not going to be
ideal as it doesn't account for the strength of the opposition properly. Don't judge too harshly as this is just
Version 1!). The distribution for the cards follows a Poisson distribution.

* Free software: Apache Software License 2.0

Installation
============

::

    pip install x-goals

Documentation
=============


To use the project:

Open a Jupyter notebook and paste the following

.. code-block:: python

    import x_goals.app as application
    xgoals_app = application.dash_app
    applic.show_app(xgoals_app)


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
