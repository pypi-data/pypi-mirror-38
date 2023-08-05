
.. image:: https://readthedocs.org/projects/invsearch/badge/?version=latest
    :target: https://invsearch.readthedocs.io/?badge=latest
    :alt: Documentation Status

.. image:: https://travis-ci.org/MacHu-GWU/invsearch-project.svg?branch=master
    :target: https://travis-ci.org/MacHu-GWU/invsearch-project?branch=master

.. image:: https://codecov.io/gh/MacHu-GWU/invsearch-project/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/MacHu-GWU/invsearch-project

.. image:: https://img.shields.io/pypi/v/invsearch.svg
    :target: https://pypi.python.org/pypi/invsearch

.. image:: https://img.shields.io/pypi/l/invsearch.svg
    :target: https://pypi.python.org/pypi/invsearch

.. image:: https://img.shields.io/pypi/pyversions/invsearch.svg
    :target: https://pypi.python.org/pypi/invsearch

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/invsearch-project

------


.. image:: https://img.shields.io/badge/Link-Document-blue.svg
      :target: https://invsearch.readthedocs.io/index.html

.. image:: https://img.shields.io/badge/Link-API-blue.svg
      :target: https://invsearch.readthedocs.io/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Source_Code-blue.svg
      :target: https://invsearch.readthedocs.io/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
      :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
      :target: https://github.com/MacHu-GWU/invsearch-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
      :target: https://github.com/MacHu-GWU/invsearch-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
      :target: https://github.com/MacHu-GWU/invsearch-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
      :target: https://pypi.org/pypi/invsearch#files


Welcome to ``invsearch`` Documentation
==============================================================================

A fast document search engine allow search by field and value pair.

Example:

.. code-block:: python

    >>> from invsearch import InvIndex
    >>> ii = InvIndex([
    ...     {"id": 1, "name": "Alice", "friends": [2, 3]},
    ...     {"id": 2, "name": "Bob", "age": 15, "friends": [1, 3]},
    ...     {"id": 3, "name": "Cathy", "age": None, "friends": [1, 2]},
    ...     {"id": 4, "name": "Bob", "age": None},
    ... ])
    >>> ii.find_one(id=1)
    {"id": 1, "name": "Alice", "friends": [2, 3]}
    >>> ii.find(name="Bob")
    [{"id": 2, "name": "Bob", "age": 15, "friends": [1, 3]}, {"id": 4, "name": "Bob", "age": None}]
    >>> ii.by_id(id=1)
    {"id": 1, "name": "Alice", "friends": [2, 3]}


.. _install:

Install
------------------------------------------------------------------------------

``invsearch`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install invsearch

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade invsearch