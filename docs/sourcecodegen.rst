.. pym documentation about Python's unparser, created by
   jalanb on Tuesday January 1st 2013

.. _sourcecodegen:

Malthe Borch's sourcecodegen
============================

Contents:

.. toctree::
   :maxdepth: 2

.. _malthes_sourcecodegen:

Links to sourcecodegen
----------------------

  * The source codegen project is stored `on github <https://github.com/malthe/sourcecodegen>`_
  * It is available `in the Cheeseshop <https://pypi.python.org/pypi/sourcecodegen/0.6.14>`_


Summary
-------

sourcecodegen is designed to worker with older versions of Python, specifically "2.4 and below", and is not compatible with the new `ast` module in Python 2.6.

It is released under the BSD license, so can be copied for investigation.

Running sourcecodegen on itself
-------------------------------

Ideally the unparser should produce itself as output, given itself as input. Let's see how it does.

Running
^^^^^^^

Run the unparser, with the commands::

    $ python2.5
    >>> from compiler import parse
    >>> tree = parse(file('visitor.py').read())
    >>> from sourcecodegen import ModuleSourceCodeGenerator
    >>> generator = ModuleSourceCodeGenerator(tree)
    >>> visitor_out = file('visitor.py', 'w')
    >>> print >> visitor_out, generator.getSourceCode()
    >>> visitor_out.close()
    >>> exit()
    $ git commit "run sourcecodegen on itself" visitor.py

Some differences are apparent in `the commit <https://github.com/jalanb/pym/commit/7305db84ede8120de3f13393ed3b792d0b583d7c#demo/sourcecoden/visitor.py>`_.

 #. Blank lines are not maintained
     In at least one case this has resulted in incorrect code, with `two lines being incorrectly joined <https://github.com/jalanb/pym/blob/7305db84ede8120de3f13393ed3b792d0b583d7c/demo/sourcecoden/visitor.py#L47479>`_.
 #. Indentation is changed from spaces to tabs
 #. Extraneous parentheses are introduced
     Some of these seem improvident, such as those `introduced around conditions of <https://github.com/jalanb/pym/blob/7305db84ede8120de3f13393ed3b792d0b583d7c/demo/sourcecoden/visitor.py#L42>`_ (some) if statements. Some return statements also `get extra parentheses <https://github.com/jalanb/pym/blob/7305db84ede8120de3f13393ed3b792d0b583d7c/demo/sourcecoden/visitor.py#L6>`_, but not `others <https://github.com/jalanb/pym/blob/7305db84ede8120de3f13393ed3b792d0b583d7c/demo/sourcecoden/visitor.py#L8>`_. Some introduced parentheses seem harmless, or even helpful, such as `introduing parentheses around a tuple <https://github.com/jalanb/pym/blob/7305db84ede8120de3f13393ed3b792d0b583d7c/demo/sourcecoden/visitor.py#L126>`_.
 #. Re-formatting of multi-line arguments for method calls to single lines

Most of the above issues seem to be matters of opinion and should be deferred to `PEP 8 <http://www.python.org/dev/peps/pep-0008/>`_. The unparser's output does seem closer to PEP8 than is its code.

Pepping
^^^^^^^

To check that the output can be run through the `pep8 tool <http://pypi.python.org/pypi/pep8>`_. I've already noticed that blank lines are removed, so we can ignore errors E301 and E302. And ignore W191 because we know indentation uses tabs::

    $ pep8 --ignore=W191,E301,E302 visitor.py
    visitor.py:8:80: E501 line too long (114 > 79 characters)
    visitor.py:84:26: E712 comparison to False should be 'if cond is False:' or 'if not cond:'
    visitor.py:108:80: E501 line too long (84 > 79 characters)
    visitor.py:469:80: E501 line too long (85 > 79 characters)
    visitor.py:479:80: E501 line too long (98 > 79 characters)
    visitor.py:480:3: E112 expected an indented block
    visitor.py:529:1: W391 blank line at end of file

This shows up some more problems

 #. Some lines are too long
 #. The final line is not correctly terminated
 #. The `code uses <https://github.com/jalanb/pym/blob/7305db84ede8120de3f13393ed3b792d0b583d7c/demo/sourcecoden/visitor.py#L84>`_ " == False", but that is not introduced by sourcecodegen itself, as it was `in the original <https://github.com/jalanb/pym/blob/b433254965df03b79363d48b44efc1e6069cb781/demo/sourcecoden/visitor.py#L105>`_.
 #. Some lines are joined, in particular pep8 notices a problem resulting from the `joining of the lines before line 480 <https://github.com/jalanb/pym/blob/7305db84ede8120de3f13393ed3b792d0b583d7c/demo/sourcecoden/visitor.py#L479>`_.

Conclusion
^^^^^^^^^^

This is not a test of sourcecodegen, just an indication of where some of its strengths/weaknesses may lie. It has one flaw (badly joined lines) which can result in unusable code, but otherwise seems robust
