===================
 icemac.songbeamer
===================

.. image:: https://travis-ci.com/icemac/icemac.songbeamer.svg?branch=master
    :target: https://travis-ci.com/icemac/icemac.songbeamer
.. image:: https://coveralls.io/repos/github/icemac/icemac.songbeamer/badge.svg?branch=master
    :target: https://coveralls.io/github/icemac/icemac.songbeamer?branch=master

Library to read and write `SongBeamer`_ files.

This package is licensed under the MIT License, see LICENSE.TXT inside the
package.

.. contents::

Supported SongBeamer versions
=============================

Currently Songbeamer versions 2 to 4 are supported. (Internal version
number in .sng files: ``#Version=3``.)

.. _`SongBeamer` : http://songbeamer.com

Supported Python version
========================

Runs only on Python 3.7. Older Python versions are not supported.

Running Tests
=============

To run the tests call::

  $ tox

(You maybe have to install `tox` beforehand using: ``pip install tox``.)

Hacking
=======

Fork me on: https://github.com:/icemac/icemac.songbeamer


=========
 Changes
=========

1.0 (2018-11-02)
================

Backwards incompatible changes
------------------------------

- The ``icemac.songbeamer.SNG`` instances no longer store the data on the
  `data` attribute but it now behaves like a ``dict`` thus allowing direct dict
  access to the data.

- It is no longer possible to use attributes on ``icemac.songbeamer.SNG``
  instances to read and store encoded bytes data. Either read/write text data
  from/to the ``icemac.songbeamer.SNG`` instance using the `dict` API or use
  the ``parse`` function (see next item) to import resp. use ``.SNG.export()``
  to export the data encoded.

- Add a function ``icemac.songbeamer.parse()`` converting a byte stream
  into a ``icemac.songbeamer.SNG`` instance. It replaces the class method on
  the `SNG` instance. It returns ``None`` if the data cannot be
  parsed and it logs an error message.

- Drop support for Python 3.5, 3.6 and PyPy3, thus only supporting Python 3.7
  now.

Features
--------

- Add a function ``icemac.songbeamer.open()`` to open a file given by a path
  and get a ``icemac.songbeamer.SNG`` instance.

- Make ``.SNG.export()`` robust against missing text in songs.

- Add a command line script `songbeamer-xls-export` exporting titles and song
  book numbers from folder containing SongBeamer files to an XLS file. To be
  able to use it `icemac.songbeamer` has to be installed with the ``xls`` extra
  like this::

    $ pip install "icemac.songbeamer[xls]"

- Support UTF-8 encoded SongBeamer files starting with the UTF-8 BOM.

- Change license from ZPL to MIT.


0.3 (2018-10-07)
================

- Add support for Python 3.5 to 3.7 and PyPy3.

- Drop support for Python 3.2 and 3.3.


0.2.0 (2012-10-31)
==================

- Add ability to parse bytes objects.

- Sorting keys in export file to be compatible across Python 3.2 and 3.3.


0.1.0 (2012-05-05)
==================

- Initial public release.




=======
 To do
=======

Implementations
===============

* import/export of .col files (schedules)


Open Questions
==============

* Are `Transpose` and `Speed` actually int values?


=======
 Usage
=======

Importing a .sng file
=====================

To import a `.sng` file use the ``open`` function in the module
``icemac.songbeamer``. It expects a filename and path and returns a SNG
instance:

  >>> import icemac.songbeamer
  >>> import pkg_resources
  >>> filename = pkg_resources.resource_filename(
  ...     'icemac.songbeamer.tests', 'example.sng')
  >>> sng = icemac.songbeamer.open(filename)
  >>> sng.__class__
  <class 'icemac.songbeamer.sng.SNG'>

Alternatively there is a function ``parse`` in the same module which parses
bytes (e. g. read from a binary file) into an SNG instance:

  >>> with open(filename, 'rb') as file:
  ...     sng = icemac.songbeamer.parse(file.read())
  >>> sng.__class__
  <class 'icemac.songbeamer.sng.SNG'>

Accessing a file's data
=======================

The SNG instance extends ``dict`` so the date is accessible via the usual
python ``dict`` API:

  >>> from pprint import pprint
  >>> pprint(sng)
  {'Author': 'me',
   'Text': ['La la la', '---', 'Lei lei lei'],
   'Version': 3}
  >>> sng['Title'] = 'Mÿ šôñg'

The values are stored as numbers resp. strings (text):

  >>> sng['Version']
  3
  >>> sng['Author']
  'me'

Exporting a .sng file
=====================

  >>> from tempfile import TemporaryFile

To export to a .sng file use the ``export`` method. It expects a byte stream
(io.BytesIO or open binary file) as argument to write into:

  >>> with TemporaryFile() as file:
  ...     sng.export(file)
  ...     _ = file.seek(0)
  ...     pprint(file.readlines())
  [b'#Author=me\r\n',
   b'#Title=M\xff \x9a\xf4\xf1g\r\n',
   b'#Version=3\r\n',
   b'---\r\n',
   b'La la la\r\n',
   b'---\r\n',
   b'Lei lei lei']


