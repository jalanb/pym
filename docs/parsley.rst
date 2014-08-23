.. pym documentation about Allen Shorts' parsley, created by
   jalanb on Friday January 11th 2014

.. _parsley_page:

Allen Shorts' parsley
=====================

Allen Shorts's `Parsley <http://parsley.readthedocs.org/en/latest/>`_ "is a pattern matching and parsing tool for Python programmers".

Links to Parsley
----------------

`Parsley <http://parsley.readthedocs.org/en/latest/>`_ follows on from Short's `Pymeta <http://washort.twistedmatrix.com/2008/03/introducing-pymeta.html>`_, and which he `introduced at Pycon 2013 <http://www.youtube.com/watch?v=t5X3ljCOFSY>`_. It is based on OMeta.

Summary
-------

Parsley is a PEG parser, which generates parsing code in Python from a grammar in OMeta.

Parsley uses `TermL <http://www.erights.org/data/terml/terml-spec.html>`_ to produce syntax trees 

Usage in pym
------------

Done:

 * Read a hosts file with parsley: `hosts.py <https://github.com/jalanb/pym/blob/master/src/parsing/parsley/hosts.py>`_ 

To Do:
 
 * Read a hosts grammar with Parsley: `meta_hosts.py <https://github.com/jalanb/pym/blob/master/src/parsing/parsley/meta_hosts.py>`_
 * Read a Parsley grammar
 * Derive a syntax tree from a Parsley-parsed text
