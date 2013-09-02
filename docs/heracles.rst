.. pym documentation about Jorge Monforte's heracles, created by
   jalanb on Monday Sptember 2nd, 2013

.. _heracles:

Jorge Monforte's heracles
============================

heracles is a project by `Jorge Monforte <http://llou.net/>`_ which can parse and render configuration files. It is based on `augeas <http://augeas.net/>`_.

.. _jorges_heracles:

Links to heracles
----------------------

* heracles is documented `on Read The Docs <https://heracles.readthedocs.org/en/latest/index.html>`_. 
* The source of the project is stored `on github <https://github.com/llou/heracles>`_.
* It is available `in the Cheeseshop <https://pypi.python.org/pypi/heracles>`_.

The code is `licensed under the LGPL <https://github.com/llou/heracles/blob/master/COPYING>`_, and so can be copied for investigation

Summary
-------

heracles is designed to work with Python2, having been specifically tested with Python2.6 and 2.7.

Like `augeas <http://augeas.net/>`_, heracles uses "lenses" which allow parsing and rendering of a variety of `common Linux configuration files <http://augeas.net/stock_lenses.html>`_. Augeas is a c-based library which also provides `Python bindings <https://github.com/hercules-team/python-augeas>`_, whereas heracles goes further in allowing straight access to the parser functions from Python

The idea of a "lens parser" is derived from `Boomerang <https://alliance.seas.upenn.edu/~harmony/>`_, and is a "well-behaved bidirectional transformation" beween text and tree, which allows re-writing parts of a file while leaving the rest of the file untouched. As such a lens parser normally has two siginificant methods: `get <https://github.com/llou/heracles/blob/master/heracles/base.py#L208>`_ and `put <https://github.com/llou/heracles/blob/master/heracles/base.py#L224>`_.

Rendering
---------

The code provides an 


Running
^^^^^^^

Run the unparser, with the commands::

    $ python2.6
    >>> from heracles import Heracles

Conclusion
^^^^^^^^^^

