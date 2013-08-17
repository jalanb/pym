.. pym documentation about Eduardo Schettino's pyregurgitator, created by
   jalanb on Tuesday January 1st 2013

.. _pyregurgitator:

Eduardo Schettino's pyregurgitator
==================================

pyregurgitator is a project by `Eduardo Schettino <http://schettino72.net/>`_ which provides tools for analysing Python code.

.. _eduardos_pyregurgitator:

Links to pyregurgitator
-----------------------

  * The pyRegurgitator project is stored `on bitbucket <https://bitbucket.org/schettino72/pyregurgitator/>`_
  * It is available `in the Cheeseshop <https://pypi.python.org/pypi/pyRegurgitator>`_

The `project page <https://bitbucket.org/schettino72/pyregurgitator/>`_ does show a TODO list, but has had no commits in a few years.

Summary
-------

pyregurgitator is intended to offer two primary tools
  * asdl2html which provides a reference table of python's ASDL
  * ast2html which provides a super pretty print of python source-code's AST

It is released under the MIT license, so can be copied for investigation.

Running pyregurgitator on itself
--------------------------------

As of version 0.1 there are three tools available 
  * ast2html which provides a super pretty print of python source-code's AST
  * ast2txt which dumps out the AST, similarly to `ast.dump <http://docs.python.org/2/library/ast.html?highlight=ast.dump#ast.dump>`_
  * ast2map which prints out the AST as a list of items, with minimal information about each

Running
^^^^^^^

Run the ast2html tool, with the commands::

    $ python2.5 bin/ast2html bin/ast2html > bin/ast2html.html

This produces `output showing the detail as the AST <http://www.al-got-rhythm.net/pym/ast2html.html>`_ of the `original source <https://bitbucket.org/schettino72/pyregurgitator/src/63dc0c9946e5/bin/ast2html>`_

Conclusion
^^^^^^^^^^

pyregurgitator is a helpful tool for anyone working with ASTs (such as myself). But it has proved not to be directly relevant to pym, as it concentrates on printing the AST, not the python. The methods it uses to pretty print the AST could yet prove informative, but details are buried in some monolithic and obscure code.

I think I shall leave investigation of pyregurgitator there.
