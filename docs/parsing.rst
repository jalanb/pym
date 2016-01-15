.. pym documentation about parsing text
    created by jalanb on Friday 22nd August 2014

.. _parsing_page:

Parsing structured text
=======================

 
.. toctree::
   :maxdepth: 1

Parsing in general is of interest. One reason for delay in starting this project has been the postponing of the choice between using Python's built-in parsing modules, or more general parsing components. Although I have now decided to start with Python's built in parser I remain open to use of other parsers as well. Not much point in having a "structured text editor" which cannot handle structured text such as other langages, marked-up texts, config files, log files, and so on.

Parsing is more than merely interesting, it is required as long as :ref:`storage` is plain.

I also intend to rely as heavily as possible on others' code in developing pym, and can only expect that to arrive hither as plain text.

Parsing Python
--------------

Parsing produces Abstract Syntax Trees, which have a reasonable amount of related documentation. Green Tree Snakes was a proximate spur to this project, and the other links in this section were found thence.

* `Green Tree Snakes - the missing Python AST docs <http://greentreesnakes.readthedocs.org/en/latest/>`_ (and some `Reddit comments <http://www.reddit.com/r/Python/comments/13kbyg/green_tree_snakes_a_new_guide_to_using_abstract/>`_ on them).
* The `Design of CPython's Compiler <http://docs.python.org/devguide/compiler.html>`_ lays out rationales behind some choices in the design of the compiler, and introduces a developer to the code supporting it. For pym it is particularly relevant in introducing `ASDL <http://www.cs.princeton.edu/research/techreps/TR-554-97>`_ and `SPARK <http://pages.cpsc.ucalgary.ca/~aycock/spark/>`_.
* `Python internals: Working with Python ASTs <http://eli.thegreenplace.net/2009/11/28/python-internals-working-with-python-asts/>`_

Parsing non-Python
------------------

Other parsers, written in Python but parsing other structures:

* :ref:`parsley_page`, which follows on from his `Pymeta <http://washort.twistedmatrix.com/2008/03/introducing-pymeta.html>`_, and which he `introduced at Pycon 2013 <http://www.youtube.com/watch?v=t5X3ljCOFSY>`_.
* Ned Batchelder's `Python parsing tools <http://nedbatchelder.com/text/python-parsers.html>`_ is a page covering many other parsers.
* Juancarlo Añez' `Grako <https://bitbucket.org/apalala/grako#templates-and-translation>`_  is "a tool that takes grammars in a variation of EBNF as input, and outputs memoizing (Packrat) PEG parsers in Python".


Meta-Compiling
--------------

`HackerNews <https://news.ycombinator.com/item?id=8297996>`_ told me about `META II <http://www.bayfronttechnologies.com/mc_tutorial.html>`_, which is able to "reproduce its own code from a description":

At the end of these steps you should be able to:

1. Define a compiler description that ejects your favorite language code
2. Paste it into the Input window
3. Have one of the compilers on these web pages generate the translation to your favorite language
4. Cut the code generated in your favorite language from the Output window
5. Continue compiler and metacompiler development in your favorite language

Unfortunately I have other work to get back to now, but the tutorial is well-written, enthusiastic about the meta-compiler, and when the tutorials don't work, it's because they are meant not to, in the next paragraph.

Excellent site, I hope to get more time on that tool.

ASTs
----

Some ideas around ASTs

* `AST Transformation Hooks for Domain Specific Languages <http://mail.python.org/pipermail/python-ideas/2011-April/009765.html>`_
* `possible meta coding in Python <https://github.com/albertz/CPython/blob/astcompile_patch/test_co_ast.py>`_
* `Reddit on pydit <http://www.reddit.com/r/Python/comments/bfnn8/pydit_im_trying_to_find_the_most_elegant_way_to/>`_
* `Reddit on ASTs (in /r/python) <http://www.reddit.com/r/Python/search?q=ast&restrict_sr=on>`_
* `NuPIC <http://numenta.org/>`_ implements cortical algorithms

Higher level structures
-----------------------

If the text to be editted is a program then parsing can be extended to include information on symbol tables, scope, control flow, tests, patterns, clichés, ...

If the text to be editted has meaning then parsing can be extended to include context, connections, importance, definition, relevance, ...
