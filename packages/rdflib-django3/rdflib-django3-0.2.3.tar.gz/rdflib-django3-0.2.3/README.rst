rdflib-django3
=============


fork from rdflib-django with multi store architecture, python3 and recent rdflib
compatibility.

A store implementation for `rdflib`_ that uses Django as its backend.

The current implementation is context-aware but not formula-aware.

The implementation assumes that contexts are used for named graphs.

.. image:: https://secure.travis-ci.org/devkral/rdflib-django3.png
   :target: https://travis-ci.org/#!/devkral/rdflib-django3

Quick start
-----------

Install rdflib-django3 with your package manager:

::

    pip install rdflib-django3

Add ``rdflib_django`` to your ``INSTALLED_APPS``:

::

    INSTALLED_APPS = (
        # other apps
        'rdflib_django'.
    )

You can now use the following examples to obtain a graph.

Getting a graph using rdflib's store API:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    from rdflib import Graph
    graph = Graph('Django', identifier="fooo")
    graph.open(create=True)

This example will give you a graph identified by a blank node within the
default store.

Getting a conjunctive graph using rdflib's store API:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    from rdflib import ConjunctiveGraph
    graph = ConjunctiveGraph('Django')

This example will give you a conjunctive graph in the default store.

Getting a named graph using rdflib-django's API:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    from rdflib_django import utils
    graph = utils.get_named_graph('http://example.com')

Getting the conjunctive graph using rdflib-django3's API:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    from rdflib_django import utils
    graph = utils.get_conjunctive_graph()

Management commands
-------------------

``rdflib-django3`` includes two management commands to import and export
RDF:

::

    $ python manage.py import_rdf --context=http://example.com my_file.rdf
    $ python manage.py export_rdf --context=http://example.com

License
-------

``rdflib-django3`` is licensed under the `MIT license`_.

.. _rdflib: http://pypi.python.org/pypi/rdflib/
.. _MIT license: https://raw.github.com/devkral/rdflib-django3/master/LICENSE
.. _MIT license: https://raw.github.com/devkral/rdflib-django/master/LICENSE.publysher
