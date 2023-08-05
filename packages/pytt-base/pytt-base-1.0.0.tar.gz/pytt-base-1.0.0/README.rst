=========
pytt-base
=========

Toutiao Base Class for Python.

Installation
============

::

    pip install pytt-base


Usage
=====

::

    In [1]: from pytt_base import BaseToutiao

    In [7]: class XXX(BaseToutiao):
       ...:     pass
       ...:

    In [3]: xxx = XXX()

    In [4]: xxx.DEVELOPER_DOMAIN
    Out[4]: 'https://developer.toutiao.com'

    In [6]: xxx._requests
    Out[6]: <bound method XXX._requests of <__main__.XXX object at 0x7f9248260d10>>

    In [7]:

