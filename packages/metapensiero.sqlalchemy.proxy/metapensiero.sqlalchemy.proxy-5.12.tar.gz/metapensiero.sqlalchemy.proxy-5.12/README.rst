.. -*- coding: utf-8 -*-
.. :Project:   metapensiero.sqlalchemy.proxy
.. :Created:   gio 30 apr 2009 10:01:20 CEST
.. :Author:    Lele Gaifax <lele@metapensiero.it>
.. :License:   GNU General Public License version 3 or later
.. :Copyright: © 2009, 2010, 2012, 2013, 2014, 2016, 2017, 2018 Lele Gaifax
..

===============================
 metapensiero.sqlalchemy.proxy
===============================

Expose SQLAlchemy's queries and their metadata to a webservice
==============================================================

This package contains a few utilities to make it easier applying some filtering to a stock
query and obtaining the resultset in various formats.

Since version 4 only Python 3 is supported: if you are still working with Python 2 (really⁈)
you may want to use `version 3.6`__ instead.

See latest documentation at http://metapensierosqlalchemyproxy.readthedocs.io/en/latest/

__ https://pypi.python.org/pypi/metapensiero.sqlalchemy.proxy/3.6

Tests suite
-----------

The tests suite is based on ``tox`` and ``pytest``: to run it simply execute

::

   $ make test

The ``PostgreSQL`` unit requires an existing database called ``mp_sa_proxy_test`` with the
``hstore`` extension, and that the current user can access it without password::

   $ createdb mp_sa_proxy_test
   $ psql -c "create extension hstore;" mp_sa_proxy_test
