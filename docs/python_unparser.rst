.. pym documentation about Python's unparser, created by
   jalanb on Tuesday January 1st 2013

.. _pythons_unparser:

Python's Unparser
=================

Contents:

.. toctree::
   :maxdepth: 2

.. _pythons_own_unparser:

Links to the unparser
---------------------

  * The unparser is a script in the `Tools/parser <http://hg.python.org/cpython/file/3f7d5c235d82/Tools/parser>`_ directory called `unparse.py <http://hg.python.org/cpython/file/3f7d5c235d82/Tools/parser/unparse.py>`_.
  * This script is a continuation from the `unparse.py file <http://hg.python.org/cpython/file/e36513032265/Demo/parser/unparse.py>`_ in the older (`2.7 <http://www.python.org/download/releases/2.7.3/>`_) `Demo/parser <http://hg.python.org/cpython/file/e36513032265/Demo/parser>`_ directory, and has been `intermittently maintained for a few years <http://hg.python.org/cpython/log/d989c3fc9e28/Demo/parser/unparse.py>`_
  * There is `a test script <http://hg.python.org/cpython/file/3f7d5c235d82/Tools/parser/test_unparse.py>`_ in the same directory, and an equivalent `test script <http://hg.python.org/cpython/file/e36513032265/Demo/parser/test_unparse.py>`_ for the 2.7 branch
  * There are some issues about it, such as `this one <http://bugs.python.org/issue14695>`_ claiming that it is out of date.

Running
-------

Run the unparser, with the commands::

    $ python unparser.py unparser.py > unparser.out
    $ diff unparser.py unparser.out

With these commands I would expect to be shown no differences, as I expected that the script should be able to reproduce itself. But some differences are apparent

 #. Comments are stripped
     This is expected.
     To my mind the problem here is that unparse.py includes any comments, but that may be a less common opinion.
 #. Docstrings are changed from double-quotes to single quotes.
     Some docstrings in unparse.py use single double-quotes, others use the (more correct) triple double-quotes. In the output both have been reduced to single-quotes
     This feature is also apparent in other strings.
 #. Blank lines are not maintained
 #. Extraneous parentheses are introduced
 #. Extra indentation is introduced at control structures
     In particular this is noticeable at if/else statements, where the original uses single-line statements for both if and else, but the unparsed version splits them over two lines. Once again the unparsed version seem more correct.

