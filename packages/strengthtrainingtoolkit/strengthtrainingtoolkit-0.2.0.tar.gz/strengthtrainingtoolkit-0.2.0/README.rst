========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |requires|
        | |coveralls| |codecov|
        | |landscape| |scrutinizer| |codacy| |codeclimate|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/python-timo's-strength-training-toolkit/badge/?style=flat
    :target: https://readthedocs.org/projects/python-timo's-strength-training-toolkit
    :alt: Documentation Status


.. |travis| image:: https://travis-ci.org/tim00w/python-timo's-strength-training-toolkit.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/tim00w/python-timo's-strength-training-toolkit

.. |requires| image:: https://requires.io/github/tim00w/python-timo's-strength-training-toolkit/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/tim00w/python-timo's-strength-training-toolkit/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/tim00w/python-timo's-strength-training-toolkit/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/tim00w/python-timo's-strength-training-toolkit

.. |codecov| image:: https://codecov.io/github/tim00w/python-timo's-strength-training-toolkit/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/tim00w/python-timo's-strength-training-toolkit

.. |landscape| image:: https://landscape.io/github/tim00w/python-timo's-strength-training-toolkit/master/landscape.svg?style=flat
    :target: https://landscape.io/github/tim00w/python-timo's-strength-training-toolkit/master
    :alt: Code Quality Status

.. |codacy| image:: https://img.shields.io/codacy/REPLACE_WITH_PROJECT_ID.svg
    :target: https://www.codacy.com/app/tim00w/python-timo's-strength-training-toolkit
    :alt: Codacy Code Quality Status

.. |codeclimate| image:: https://codeclimate.com/github/tim00w/python-timo's-strength-training-toolkit/badges/gpa.svg
   :target: https://codeclimate.com/github/tim00w/python-timo's-strength-training-toolkit
   :alt: CodeClimate Quality Status

.. |version| image:: https://img.shields.io/pypi/v/strengthtrainingtoolkit.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/strengthtrainingtoolkit

.. |commits-since| image:: https://img.shields.io/github/commits-since/tim00w/python-timo's-strength-training-toolkit/v0.2.0.svg
    :alt: Commits since latest release
    :target: https://github.com/tim00w/python-timo's-strength-training-toolkit/compare/v0.2.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/strengthtrainingtoolkit.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/strengthtrainingtoolkit

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/strengthtrainingtoolkit.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/strengthtrainingtoolkit

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/strengthtrainingtoolkit.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/strengthtrainingtoolkit

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/g/tim00w/python-timo's-strength-training-toolkit/master.svg
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/tim00w/python-timo's-strength-training-toolkit/


.. end-badges

Timo's Strength Training Toolkit. Grow strong!

* Free software: MIT license

Installation
============

::

    pip install strengthtrainingtoolkit

Documentation
=============


https://python-timo's-strength-training-toolkit.readthedocs.io/


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
