.. pym documentation about Python's unparser, created by
   jalanb on Tuesday January 1st 2013

.. _pythons_unparser:

Python's Unparser
=================

The source for python includes an unparser, which can render ASTs to source.

.. _pythons_own_unparser:

Links to the unparser
---------------------

* The unparser is a script in the `Tools/parser <http://hg.python.org/cpython/file/3f7d5c235d82/Tools/parser>`_ directory called `unparse.py <http://hg.python.org/cpython/file/3f7d5c235d82/Tools/parser/unparse.py>`_.
* This script is a continuation from the `unparse.py file <http://hg.python.org/cpython/file/e36513032265/Demo/parser/unparse.py>`_ in the older (`2.7 <http://www.python.org/download/releases/2.7.3/>`_) `Demo/parser <http://hg.python.org/cpython/file/e36513032265/Demo/parser>`_ directory, and has been `intermittently maintained for a few years <http://hg.python.org/cpython/log/d989c3fc9e28/Demo/parser/unparse.py>`_
* There is `a test script <http://hg.python.org/cpython/file/3f7d5c235d82/Tools/parser/test_unparse.py>`_ in the same directory, and an equivalent `test script <http://hg.python.org/cpython/file/e36513032265/Demo/parser/test_unparse.py>`_ for the 2.7 branch
* There are some issues about it, such as `this one <http://bugs.python.org/issue14695>`_ claiming that it is out of date.

Rendering
---------

The code provides an `Unparser class <http://hg.python.org/cpython/file/3f7d5c235d82/Tools/parser/unparse.py#l25>`_, which contains `a method <http://hg.python.org/cpython/file/3f7d5c235d82/Tools/parser/unparse.py#l259>`_ for each type of node. The methods render their own node's code, and call sub-nodes's methods sending in the respective nodes.

Running the unpraser on itself
------------------------------

Ideally the unparser should produce itself as output, given itself as input. Let's see how it does.

Running
^^^^^^^

Run the unparser, with the commands::

    $ python2.7 unparse.py unparse.py > unparse.out.py
    $ diff unparse.py unparse.out.py

.. _python_unparser_output:

Some differences are apparent

 #. Comments are stripped
     This is expected.
     To my mind the problem here is that unparse.py includes any comments (but that may be a less common opinion).
 #. Docstrings are changed from double-quotes to single quotes.
     Some docstrings in unparse.py use single double-quotes, others use the (`PEP 8 recommendation of <http://www.python.org/dev/peps/pep-0008/#documentation-strings>`_) triple double-quotes. In the output both have been reduced to single-quotes

     This feature is also apparent in other strings.
 #. Blank lines are not maintained
 #. Extraneous parentheses are introduced
     Some of these seem improvident, such as those introduced around conditions of (some) if statements. Others seem harmless, or even helpful, such as introducing parentheses around a literal tuple. Introducing parentheses around expressions after a print statement is dubious, given that I used python 2, not 3.
 #. Extra indentation is introduced at control structures
     In particular this is noticeable at if/else statements, where the original uses compound statements for both if and else, but the unparsed version splits them over two lines. Once again the unparsed version seems `more correct <http://www.python.org/dev/peps/pep-0008/#other-recommendations>`_.
 #. Re-formatting of a multi-line dictionary to a single line
 #. Re-formatting expressions to introduce spaces around operators

Most of the above issues seem to be matters of opinion and should be deferred to `PEP 8 <http://www.python.org/dev/peps/pep-0008/>`_. The unparser's output does seem closer to PEP8 than is its code.

Pepping
^^^^^^^

To check that the output can be run through the `pep8 tool <http://pypi.python.org/pypi/pep8>`_. I've already noticed that blank lines and spaces around some operators aren't handled optimally, so I'll ask pep8 to ignore errors 302 and 203::

    $ pep8 --ignore=E302,E203 unparse.out.py
    unparse.out.py:22:80: E501 line too long (150 > 79 characters)
    unparse.out.py:25:80: E501 line too long (95 > 79 characters)
    unparse.out.py:255:80: E501 line too long (86 > 79 characters)
    unparse.out.py:383:80: E501 line too long (82 > 79 characters)
    unparse.out.py:408:80: E501 line too long (180 > 79 characters)
    unparse.out.py:416:80: E501 line too long (150 > 79 characters)
    unparse.out.py:573:23: W292 no newline at end of file

This shows up two more problems

 #. Some lines are too long
 #. The final line is not correctly terminated

Conclusion
^^^^^^^^^^

This is not a test of the unparser, just an indication of where some of its strengths/weaknesses may lie. It did not show up any fatal flaws, but does suggest the unparser needs some (small) work to get it's own code to meet PEP 8 standards.

This quick run through also shows up the fact that "what code should look like" is a very opinionated subject. Python is lucky to have PEP 8 as a standard to refer to, but even that allows for variations (only "new code" need use spaces, for example). Which shows up one further bug in the unparser: all its formatting choices are hard-coded, whereas we may need greater flexibility in such choices.
