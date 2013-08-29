.. pym documentation about rendering text
    created by jalanb on Thursday 9th May 2013

.. _renderers:

Rendering code
==============

In order to be more easily read AST trees can pretty printed (`a.k.a. <http://en.wiktionary.org/wiki/AKA#English>`_ rendered).
Some other code which may be helpful in rendering AST trees as Python text are
 
.. toctree::
   :maxdepth: 1

   python_unparser
   sourcecodegen
   pyregurgitator
   python_decompiler
   approach

Python renderers of Python ASTs
-------------------------------

 * :ref:`pythons_unparser`
 * :ref:`sourcecodegen`

Python renderers of other trees
-------------------------------

 * :ref:`pyregurgitator`
 * :ref:`approach`
 * Jorge Monforte's `heracles <https://github.com/llou/heracles>`_ is based on Augeas
 * Guillaume Bour's `reblok <http://devedge.bour.cc/wiki/Reblok>`_ builds ASTs from bytecode
 * Cenk Alti's `pythml <https://github.com/cenkalti/pyhtml>`_ renders html from method calls
 

Other renderers of other trees
------------------------------

 * `Augeas <http://augeas.net/index.html>`_
  


To Do
-----

A significant initial task shall be to evaluate these renderers:
  * find their commonalities
  * find their idiosyncracies
  * decide on my own rendering strategy.

