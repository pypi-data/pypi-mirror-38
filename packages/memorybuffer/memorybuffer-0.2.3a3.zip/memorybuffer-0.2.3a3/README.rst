memorybuffer
============

Python buffer protocol.

Overview
========

  | Provides routines to implement `Python Buffer Protocol`_ in clean Python
  | instead of C extension class.
  | TODO...

Installation
============

Prerequisites:

+ Python 2.7 or higher

  * http://www.python.org/
  * 2.7 and 3.4 are primary test environments.

+ pip and setuptools

  * http://pypi.python.org/pypi/pip
  * http://pypi.python.org/pypi/setuptools

To install run::

    python -m pip install --upgrade memorybuffer

Development
===========

Visit `development page <https://github.com/karpierz/memorybuffer>`__

Installation from sources:

Clone the `sources <https://github.com/karpierz/memorybuffer>`__ and run::

    python -m pip install ./memorybuffer

or on development mode::

    python -m pip install --editable ./memorybuffer

Prerequisites:

+ Development is strictly based on *tox*. To install it run::

    python -m pip install tox

License
=======

  | Copyright (c) 2012-2018 Adam Karpierz
  |
  | Licensed under the zlib/libpng License
  | http://opensource.org/licenses/zlib
  | Please refer to the accompanying LICENSE file.

Authors
=======

* Adam Karpierz <adam@karpierz.net>

.. _`Python Buffer Protocol`: https://docs.python.org/3/c-api/buffer.html
