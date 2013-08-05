.. pym documentation master file, created by
   sphinx-quickstart on Mon Dec 24 01:47:53 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _pym_index:

pym v0.0.1 documentation
========================

Parts of the documentation:

.. toctree::
   :maxdepth: 1

   renderers

What is pym?
------------

pym is an editor for structured text, in particular for Python source code. pym was inspired by vim but it handles structured (not plain) text.

At present pym is entirely vapourware, and consists of some ideas based around manipulation of `Abstract Syntax Trees <http://en.wikipedia.org/wiki/Abstract_syntax_tree>`_, such as those handled by the `ast module <http://docs.python.org/2/library/ast.html?highlight=ast>`_ .

Rendering code
^^^^^^^^^^^^^^

In order to be more easily read AST trees can pretty printed (`a.k.a. <http://en.wiktionary.org/wiki/AKA#English>`_ rendered). Some other code which may be helpful in rendering AST trees as Python text are documented in :ref:`renderers`
 
Parsing
^^^^^^^

Parsing in general is of interest. One reason for delay in starting this project has been the postponing of the choice between using Python's built-in parsing modules, or more general parsing components. Although I have now decide to start with Python's built in parser I remain committed to use of other parser. Not much point in having a "structured text editor" which cannot handle structured text such as other langages, marked-up texts, config files, log files, and so on.

Other parsers, written in Python but parsing other structures.

 * `Ned Batchelder's Python parsing tools <http://nedbatchelder.com/text/python-parsers.html>`_
 * `C parser and AST generator written in Python <http://code.google.com/p/pycparser/>`_
 * `PyPlus <http://www.reddit.com/r/Python/comments/wv6qn/plyplus_a_friendly_yet_powerful_lrparser_written/>`_
 * `/r/parsing <http://www.reddit.com/r/parsing>`_
 * `CodeTalker <http://pypi.python.org/pypi/CodeTalker/0.5>`_


Parsing produces Abstract Syntax Trees, which have a reasonable amount of related documentation. Green Tree Snakes was a proximate spur to this project, and the other links in this section were found thence.


 * `Green Tree Snakes - the missing Python AST docs <http://greentreesnakes.readthedocs.org/en/latest/>`_
 * `Reddit on Green Tree Snakes <http://www.reddit.com/r/Python/comments/13kbyg/green_tree_snakes_a_new_guide_to_using_abstract/>`_
 * `Python internals: Working with Python ASTs <http://eli.thegreenplace.net/2009/11/28/python-internals-working-with-python-asts/>`_
 * `AST Transformation Hooks for Domain Specific Languages <http://mail.python.org/pipermail/python-ideas/2011-April/009765.html>`_
 * `possible meta coding in Python <https://github.com/albertz/CPython/blob/astcompile_patch/test_co_ast.py>`_
 * `Reddit on pydit <http://www.reddit.com/r/Python/comments/bfnn8/pydit_im_trying_to_find_the_most_elegant_way_to/>`_
 * `Reddit on ASTs (in /r/python) <http://www.reddit.com/r/Python/search?q=ast&restrict_sr=on>`_

Related tools
^^^^^^^^^^^^^

Autopep8 is a tool which re-writes Python source code (to increase compliance with PEP8), but does not use ASTs to do so.

  * `autopep8 <https://github.com/jalanb/autopep8>`_

Miscellaneous
^^^^^^^^^^^^^

Other stuff I have read recently

  * `Static Modification of Python With Python: The AST Module <http://blueprintforge.com/blog/2012/02/27/static-modification-of-python-with-python-the-ast-module/>`_
  * `Coding in a debugger <http://msinilo.pl/blog/?p=965>`_
  * `DMS® Software Reengineering Toolki <http://www.semanticdesigns.com/Products/DMS/DMSToolkit.html>`_
  * `Recognition can be harder than parsing <http://www.academia.edu/798690/Recognition_can_be_harder_than_parsing>`_

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

