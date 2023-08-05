======
tinysa
======


.. image:: https://img.shields.io/pypi/v/tinysa.svg
        :target: https://pypi.python.org/pypi/tinysa

.. image:: https://img.shields.io/travis/jun-harashima/tinysa.svg
        :target: https://travis-ci.org/jun-harashima/tinysa

tinysa is a minimal implementation for constructing a suffix array.

Quick Start
===========

To install tinysa, run this command in your terminal:

.. code-block:: bash

   $ pip install tinysa

Using tinysa, you can construct a suffix array as follows:

.. code-block:: python

   from tinysa.tinysa import TinySA

   suffix_array = TinySA()
   suffix_array.index('banana')

Then, you can find a suffix that begins with a substring as follows:

.. code-block:: python

   position = suffix_array.search('ana')
   print(position)  # => 1
