=========
pybd-base
=========

Baidu XiongZhang Base Class for Python.

Installation
============

::

    pip install pybd-base


Usage
=====

::

    In [1]: from pybd-base import BaseBaidu

    In [7]: class XXX(BaseBaidu):
       ...:     pass
       ...:

    In [3]: xxx = XXX()

    In [4]: xxx.OPENAPI
    Out[4]: 'https://openapi.baidu.com'

    In [6]: xxx._requests
    Out[6]: <bound method XXX._requests of <__main__.XXX object at 0x7f9248260d10>>

    In [7]:

