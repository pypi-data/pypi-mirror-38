========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|



.. |travis| image:: https://travis-ci.org/sherwinski/palette-tools.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/sherwinski/palette-tools

.. |codecov| image:: https://codecov.io/github/sherwinski/palette-tools/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/sherwinski/palette-tools

.. |version| image:: https://img.shields.io/pypi/v/palettetools.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/palettetools

.. |commits-since| image:: https://img.shields.io/github/commits-since/sherwinski/palette-tools/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/sherwinski/palette-tools/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/palettetools.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/palettetools

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/palettetools.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/palettetools

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/palettetools.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/palettetools


.. end-badges

A Python library for extracting and analyzing color palettes from images.
All images must be served through Imgix, more information can be found at http://www.imgix.com.

* Free software: BSD 2-Clause License

Installation
============

::

    pip install palettetools

Documentation
=============


To use the project:

.. code-block:: python

    import palettetools as pt
    url = "https://assets.imgix.net/examples/bluehat.jpg"

    print pt.extract_colors_css(url)
    print pt.extract_colors_json(url)
    print pt.overlaid_text_color(url)

Testing
===========

To run the all tests run::

    tox
