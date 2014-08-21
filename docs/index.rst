.. pym documentation master file, created by
   sphinx-quickstart on Mon Dec 24 01:47:53 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _pym_index:

pym v0.1.3 documentation
========================

Parts of the documentation:

.. toctree::
   :maxdepth: 1

   renderers

What is pym?
------------

pym is an editor for structured text.

pym was inspired by vim but it handles structured (not plain) text. At present pym is entirely vapourware, and consists of some ideas based around :ref:`mindful_manipulation` of `Abstract Syntax Trees <http://en.wikipedia.org/wiki/Abstract_syntax_tree>`_, such as those handled by the `ast module <http://docs.python.org/2/library/ast.html?highlight=ast>`_ .

Rendering code
^^^^^^^^^^^^^^

In order to be more easily read AST trees can pretty printed (`a.k.a. <http://en.wiktionary.org/wiki/AKA#English>`_ rendered). Some other projects which may be helpful in rendering ASTs as plain text are documented in :ref:`renderers`
 
Parsing
^^^^^^^

Parsing in general is of interest. One reason for delay in starting this project has been the postponing of the choice between using Python's built-in parsing modules, or more general parsing components. Although I have now decided to start with Python's built in parser I remain open to use of other parsers as well. Not much point in having a "structured text editor" which cannot handle structured text such as other langages, marked-up texts, config files, log files, and so on.

Other parsers, written in Python but parsing other structures:

* :ref:`parsley_page`, which follows on from his `Pymeta <http://washort.twistedmatrix.com/2008/03/introducing-pymeta.html>`_, and which he `introduced at Pycon 2013 <http://www.youtube.com/watch?v=t5X3ljCOFSY>`_.
* Ned Batchelder's `Python parsing tools <http://nedbatchelder.com/text/python-parsers.html>`_ is a page covering many other parsers.
* Juancarlo Añez' `Grako <https://bitbucket.org/apalala/grako#templates-and-translation>`_  is "a tool that takes grammars in a variation of EBNF as input, and outputs memoizing (Packrat) PEG parsers in Python".


Parsing produces Abstract Syntax Trees, which have a reasonable amount of related documentation. Green Tree Snakes was a proximate spur to this project, and the other links in this section were found thence.

* `Green Tree Snakes - the missing Python AST docs <http://greentreesnakes.readthedocs.org/en/latest/>`_ (and some `Reddit comments <http://www.reddit.com/r/Python/comments/13kbyg/green_tree_snakes_a_new_guide_to_using_abstract/>`_ on them).
* The `Design of CPython's Compiler <http://docs.python.org/devguide/compiler.html>`_ lays out rationales behind some choices in the design of the compiler, and introduces a developer to the code supporting it. For pym it is particularly relevant in introducing `ASDL <http://www.cs.princeton.edu/research/techreps/TR-554-97>`_ and `SPARK <http://pages.cpsc.ucalgary.ca/~aycock/spark/>`_.
* `Python internals: Working with Python ASTs <http://eli.thegreenplace.net/2009/11/28/python-internals-working-with-python-asts/>`_
* `AST Transformation Hooks for Domain Specific Languages <http://mail.python.org/pipermail/python-ideas/2011-April/009765.html>`_
* `possible meta coding in Python <https://github.com/albertz/CPython/blob/astcompile_patch/test_co_ast.py>`_
* `Reddit on pydit <http://www.reddit.com/r/Python/comments/bfnn8/pydit_im_trying_to_find_the_most_elegant_way_to/>`_
* `Reddit on ASTs (in /r/python) <http://www.reddit.com/r/Python/search?q=ast&restrict_sr=on>`_
* `NuPIC <http://numenta.org/>`_ implements cortical algorithms

Related tools
^^^^^^^^^^^^^

Autopep8 is a tool which re-writes Python source code (to increase compliance with PEP8), but does not use ASTs to do so.

  * `autopep8 <https://github.com/jalanb/autopep8>`_

Miscellaneous
^^^^^^^^^^^^^

Other stuff I have read recently

* In `Invertible Syntax Descriptions: Unifying Parsing and Pretty Printing (pdf) <http://www.informatik.uni-marburg.de/~rendel/unparse/rendel10invertible.pdf>`_ Tillmann Rendel & Klaus Ostermann propose a method for writing parsers such that pretty printers can be written in the same manner. I do not have enough knowledge of their academic context to appreciate it; but the idea of "invertible syntax" descriptions strikes a chord. It does seem reasonable that if one can parse from "A" into "B", then one should be able to render from "B" to "A".
* `LL and LR in Context: Why Parsing Tools Are Hard <http://blog.reverberate.org/2013/09/ll-and-lr-in-context-why-parsing-tools.html>`_ introduced me to the notion of undecidably ambiguous grammars and the common strategies for getting around them.
* Martin Fowler distinguishes between Concrete and Abstract syntax trees when discussing `language workbenches <http://martinfowler.com/articles/languageWorkbench.html>`_.
* Laurence Tratt rememebers that SDEs are Syntax directed editing tools and that `when seasoned programmers were asked to use SDE tools, they revolted against the huge decline in their productivity <http://tratt.net/laurie/blog/entries/an_editor_for_composed_programs>`_, but that does not discouarge him from introducing `Eco, an editor for language composition <https://bitbucket.org/softdevteam/eco>`_.


Other stuff I need to read
^^^^^^^^^^^^^^^^^^^^^^^^^^

* C parser and AST generator written in Python: `pycparser <http://code.google.com/p/pycparser/>`_.
* `PyPlus <http://www.reddit.com/r/Python/comments/wv6qn/plyplus_a_friendly_yet_powerful_lrparser_written/>`_.
* `CodeTalker <http://pypi.python.org/pypi/CodeTalker>`_.
* Reddit always has much to say, so `/r/parsing will too <http://www.reddit.com/r/parsing/>`_.
* Python uses `Zephyr Abstract Syntax Description Language <http://www.cs.princeton.edu/research/techreps/TR-554-97>`_ to specify ASTs.
* :ref:`parsley_page` uses `TermL <http://www.erights.org/data/terml/terml-spec.html>`_ to specify ASTs.
* Python uses `SPARK <http://pages.cpsc.ucalgary.ca/~aycock/spark/>`_, which is a Scanning, Parsing, and Rewriting Kit.
* There is a version of `Ometa in Javascript <http://b-studios.github.io/ometa-js/>`_.
* `Static Modification of Python With Python: The AST Module <http://blueprintforge.com/blog/2012/02/27/static-modification-of-python-with-python-the-ast-module/>`_.
* Sounds like fun: `Coding in a debugger <http://msinilo.pl/blog/?p=965>`_.
* `Ira Baxter <http://www.semanticdesigns.com/Company/People/idbaxter/index.html>`_ often turns up on forums I read, usually claiming that this is going to be `harder <http://stackoverflow.com/a/3460977/500942>`_ than I think. He may have `a point <http://www.semanticdesigns.com/Products/DMS/LifeAfterParsing.html>`_! (Alternatively, as an actress asked: `Have you ever noticed how "What the hell!" is always the right decision to make? <http://www.imdb.com/title/tt0089343/quotes?item=qt2146968>`_)
* `Recognition can be harder than parsing <http://www.academia.edu/798690/Recognition_can_be_harder_than_parsing>`_.
* KOD has an interesting `approach to text syntax trees (TST) <https://github.com/rsms/kod/wiki/Text-parser-2>`_.
* The Program Transformation `Wiki <http://www.program-transformation.org/>`_.
* The `AST Tool Box <https://github.com/chick/ast_tool_box>`_ looks like it is under active development

Version 2.0 +
-------------

* ACE was `A Cliche-based Program Structure Editor (pdf) <http://dspace.mit.edu/bitstream/handle/1721.1/41181/AI_WP_294.pdf>`_. Clichés are higher branches of the (AS) tree, or collections of branches, and are closer to what editors are actually thinking about. Ultimately one would prefer to "replace the switch with inheritance", not twiddle about with nodes and branches.
* One should be prepared to move beyond the standard flat represenation of text, to `3D Treemaps (pdf) <http://www.sm.luth.se/csee/csn/publications/APCHI04Web.pdf>`_, especially `Interactive Rendering of 3D Treemaps (pdf) <http://www.hpi.uni-potsdam.de/fileadmin/hpi/FG_Doellner/publications/2013/TSD2013/TreeMap.pdf>`_.
* (Like many others) I think Bret Victor is right about `Learnable Programming <http://worrydream.com/LearnableProgramming/>`_.

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

