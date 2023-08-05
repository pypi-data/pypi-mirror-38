tdtypes
=======

.. image:: https://img.shields.io/pypi/v/tdtypes.svg
     :target: https://pypi.python.org/pypi/tdtypes
     :alt: PyPi
.. image:: https://img.shields.io/badge/License-MIT-blue.svg
     :target: https://opensource.org/licenses/MIT
     :alt: MIT License
.. image:: https://img.shields.io/pypi/pyversions/tdtypes.svg
     :alt: Python3.6+

`tdtypes <https://bitbucket.org/padhia/tdtypes>`_ is a Python library built atop `DB API <https://www.python.org/dev/peps/pep-0249/>`_ compliant library that provides abstraction layer for Teradata Database objects and utilities.

*NOTES:*

- This library was originally developed as a personal project. It is being made available as an open-source project in the hope that someone else might find it useful. This library does not come with any expressed or implied warranty.
- *Python2* series is no longer supported.
- Use of older `teradata <https://pypi.python.org/pypi/teradata/>`_ and `pyodbc <https://github.com/mkleehammer/pyodbc>`_ modules has been deprecated.
- This library is not endorsed by `Teradata Inc <http://www.teradata.com/>`_.

Installation
------------

Use Python's ``pip`` utility to install ``tdtypes``.

::

  $ python -m pip install -U tdtypes

Customization
-------------

**tdtypes** module provides two ways to get connection information from end users. End users can supply connection information by either``--tdconn`` command-line option, or set ``TDCONN`` environment variable. Connection information consists of a valid JSON string as expected by `teradatasql <https://pypi.org/project/teradatasql/>`_. See the supplied sample script.

It is possible to customize the way connection information is obtained. This can be helpful, for example, to use DB API modules other than the default ``teradatasql``, or use LDAP or SSO authentication. This can be done by creating **tdconn_site.py** module and place it in your ``PYTHONPATH``. Please consult the default *tdconn_default.py* module for guidance on creating your own custom module.

Support
-------

If you encounter an issue, report it using `issue tracker <https://bitbucket.org/padhia/tdtypes/issues?status=new&status=open>`_. I'll try to provide a fix as soon as I can. If you already have a fix, send me a pull request.

Contributions
-------------

Feel free to fork this repository and enhance it in a way you see fit. If you think your changes will benefit more people, send me a pull request.
