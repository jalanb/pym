.. pym documentation catch-all
    created by jalanb on Friday 22nd August 2014

.. _miscellaneous:

Miscellaneous
=============

.. toctree::
   :maxdepth: 1

This page is mainly a grab-bag of interesting links which have given me some of the ideas behind pym.

Other stuff I have read
^^^^^^^^^^^^^^^^^^^^^^^

* In `Invertible Syntax Descriptions: Unifying Parsing and Pretty Printing (pdf) <http://www.informatik.uni-marburg.de/~rendel/unparse/rendel10invertible.pdf>`_ Tillmann Rendel & Klaus Ostermann propose a method for writing parsers such that pretty printers can be written in the same manner. I do not have enough knowledge of their academic context to appreciate it; but the idea of "invertible syntax" descriptions strikes a chord. It does seem reasonable that if one can parse from "A" into "B", then one should be able to render from "B" to "A".
* `LL and LR in Context: Why Parsing Tools Are Hard <http://blog.reverberate.org/2013/09/ll-and-lr-in-context-why-parsing-tools.html>`_ introduced me to the notion of undecidably ambiguous grammars and the common strategies for getting around them.
* Martin Fowler distinguishes between Concrete and Abstract syntax trees when discussing `language workbenches <http://martinfowler.com/articles/languageWorkbench.html>`_.
* Laurence Tratt rememebers that SDEs are Syntax directed editing tools and that `when seasoned programmers were asked to use SDE tools, they revolted against the huge decline in their productivity <http://tratt.net/laurie/blog/entries/an_editor_for_composed_programs>`_, but that does not discouarge him from introducing `Eco, an editor for language composition <https://bitbucket.org/softdevteam/eco>`_. (I liked `/u/chrisdoner's <http://www.reddit.com/user/chrisdoner>`_ `contribution <http://www.reddit.com/r/programming/comments/2e2hfo/an_editor_for_composed_programs/cjvyx5l>`_ to the reddit `discussion <http://www.reddit.com/r/programming/comments/2e2hfo/an_editor_for_composed_programs/>`_).


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

Related tools
^^^^^^^^^^^^^

* `Autopep8 <https://github.com/jalanb/autopep8>`_ is a tool which re-writes Python source code (to increase compliance with PEP8), but does not use ASTs to do so.
* `py.code <http://pylib.readthedocs.org/en/latest/code.html>`_ provides higher level python code and introspection objects.
* `Lamdu <http://peaker.github.io/lamdu/>`_ aims to "create a next-generation live programming environment". Their ambitions are wider than mine, but we start from similar problems.

Version 2.0 +
-------------

* ACE was `A Cliche-based Program Structure Editor (pdf) <http://dspace.mit.edu/bitstream/handle/1721.1/41181/AI_WP_294.pdf>`_. Clichés are higher branches of the (AS) tree, or collections of branches, and are closer to what editors are actually thinking about. Ultimately one would prefer to "replace the switch with inheritance", not twiddle about with nodes and branches.
* One should be prepared to move beyond the standard flat represenation of text, to `3D Treemaps (pdf) <http://www.sm.luth.se/csee/csn/publications/APCHI04Web.pdf>`_, especially `Interactive Rendering of 3D Treemaps (pdf) <http://www.hpi.uni-potsdam.de/fileadmin/hpi/FG_Doellner/publications/2013/TSD2013/TreeMap.pdf>`_.
* (Like many others) I think Bret Victor is right about `Learnable Programming <http://worrydream.com/LearnableProgramming/>`_.

