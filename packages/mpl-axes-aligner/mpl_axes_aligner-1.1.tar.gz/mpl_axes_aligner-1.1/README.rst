=======================
Matplotlib Axes Aligner
=======================

.. image:: https://travis-ci.org/ryutok/mpl_axes_aligner.svg?branch=master
   :target: https://travis-ci.org/ryutok/mpl_axes_aligner
.. image:: https://api.codeclimate.com/v1/badges/86a7122db1585d63fcb9/maintainability
   :target: https://codeclimate.com/github/ryutok/mpl_axes_aligner/maintainability
   :alt: Maintainability
.. image:: https://api.codeclimate.com/v1/badges/86a7122db1585d63fcb9/test_coverage
   :target: https://codeclimate.com/github/ryutok/mpl_axes_aligner/test_coverage
   :alt: Test Coverage
.. image:: https://img.shields.io/pypi/v/nine.svg
   :target: https://pypi.org/project/mpl-axes-aligner/
   :alt: PyPI
.. image:: https://readthedocs.org/projects/matplotlib-axes-aligner/badge/?version=latest
   :target: https://matplotlib-axes-aligner.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
.. image:: http://img.shields.io/badge/license-MIT-blue.svg?style=flat
   :target: https://github.com/ryutok/mpl_axes_aligner/blob/master/LICENSE


Overview
========

*Matplotlib axes aligner* (``mpl_axes_aligner``) package contains the modules which adjust the plotting range of `matplotlib.axes.Axes <https://matplotlib.org/api/axes_api.html#matplotlib.axes.Axes>`_ objects to align their origins.

- ``mpl_axes_aligner.shift`` expands or shifts the plotting range of a matplotlib axis to align the origin with the given position.
- ``mpl_axes_aligner.align`` adjust the plotting range of two matplotlib axes to align their origins with the given position.


Usage
=====

::

   import numpy as np
   import matplotlib.pyplot as plt
   import mpl_axes_aligner

   x = np.arange(0.0, 30, 0.1)
   y1 = 0.1 * x * np.sin(x)
   y2 = 0.001*x**3 - 0.03*x**2 + 0.12*x

   fig = plt.figure()
   ax1 = fig.add_subplot(111)
   ax2 = ax1.twinx()

   ax1.plot(x, y1, color='blue', label='Plot 1')
   ax2.plot(x, y2, color='red', label='Plot 2')

   # Align y = 0 of ax1 and ax2 with the center of figure.
   mpl_axes_aligner.align.yaxes(ax1, 0, ax2, 0, 0.5)

   plt.show()

.. image:: https://github.com/ryutok/mpl_axes_aligner/blob/master/docs/img/intro_plt.png?raw=true


Documentation
=============

https://matplotlib-axes-aligner.rtfd.io


Installation
============
Install from `PyPI <https://pypi.org/project/mpl-axes-aligner/>`_::

  pip install mpl-axes-aligner


Requirements
============

- Python == 2.7, 3.4, 3.5, 3.6
- Matplotlib == 2.2, 3.0

Python 3.7 may be available, but it is not checked.


License
=======

`MIT License <https://github.com/ryutok/mpl_axes_aligner/blob/master/LICENSE>`_


Author
======

`ryutok <https://github.com/ryutok>`_
