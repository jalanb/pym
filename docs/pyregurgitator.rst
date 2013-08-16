.. pym documentation about Eduardo Schettino's pyregurgitator, created by
   jalanb on Tuesday January 1st 2013

.. _pyregurgitator:

Eduardo Schettino's pyregurgitator
==================================

pyregurgitator is a project by `Eduardo Schettino <http://schettino72.net/>`_ which provides tools for analysing Python code.

.. _eduardos_pyregurgitator:

Links to pyregurgitator
----------------------

  * The pyRegurgitator project is stored `on bitbucket <https://bitbucket.org/schettino72/pyregurgitator/>`_
  * It is available `in the Cheeseshop <https://pypi.python.org/pypi/pyRegurgitator>`_

Summary
-------

pyregurgitator is intended to offer two primary tools
  * asdl2html which provides a reference table of python's ASDL
  * ast2html which provides a super pretty print of python source-code's AST

It is released under the MIT license, so can be copied for investigation.

Running pyregurgitator on itself
-------------------------------

As of version 0.1 the only tool available is `ast2html`

Running
^^^^^^^

Run the ast2html tool, with the commands::

    $ python2.5 bin/ast2html bin/ast2html > bin/ast2html.html

Conclusion
^^^^^^^^^^

This is not a test of pyregurgitator, just an indication of where some of its strengths/weaknesses may lie.
