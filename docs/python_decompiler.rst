.. pym documentation about Warbo's Python-Decompiler, created by
   jalanb on Tuesday, August 27th 2013

.. _pythondecompiler:

Chris Warburton's Python-Decompiler
===================================

Python-Decompiler is a project by `Chris Warburton <http://chriswarbo.net/>`_ which can generate source code from ASTs.

.. _warbo_pythondecompiler:

Links to Python-Decompiler
--------------------------

* The most recent form of the project is stored `on gitorious <https://gitorious.org/python-decompiler>`_.
* A previous version was stored `on Github <https://github.com/Warbo/Python-Decompiler>`_ (whence `I forked it <https://github.com/jalanb/Python-Decompiler>`_ while working with `PyMeta <https://launchpad.net/pymeta>`_).

Summary
-------

The Python-Decompiler project includes a directory called `python_rewriter <https://gitorious.org/python-decompiler/python_rewriter/source/b263c45ad84a737422ee8e35f9e2f3a30cc28e56:python_rewriter>`_ which defines `an OMeta grammar <https://gitorious.org/python-decompiler/python_rewriter/source/b263c45ad84a737422ee8e35f9e2f3a30cc28e56:python_rewriter/base.py#L122>`_ to parse Python's ASTs and thence render Python code. it is based on the ASTs of the 2.x `compiler module <http://docs.python.org/2/library/compiler.html>`_

It is released into the Public Domain, so can be copied for investigation.

Rendering
---------


Running Python-Decompiler on itself
-----------------------------------


Running
^^^^^^^

Run the unparser, with the commands::

    $ python
    >>> from python_rewriter import base
    >>> from helpers.indent_lists import indented
    >>> reload(base)
    >>> source_text = file(source).read()
    >>> parsed_source = base.parse(source_text)
    >>> parsed_sources = [parsed_source]
    >>> prettied_sources = pformat(parsed_sources)
    >>> file('nodes.py','w').write(prettied_sources)
    >>> indented_source = indented(parsed_sources)
    >>> file('indents.py','w').write(indented_source)
    >>> grammared_sources = base.grammar(parsed_sources)
    >>> pythoned_sources = grammared_sources.apply('python', 0)
    >>> text = pythoned_sources[0]
    >>> file(out,'w').write(text)

Some differences are apparent

 #. Comments are stripped
     This is expected.
 #. Leading tabs are converted to spaces.
     This is unsurprising, but not in the spirit of PEP 8's distinction about "new code"
 #. Some extra blank lines are added
 #. Extraneous parentheses are introduced
     Some of these seem improvident, such as those introduced around conditions of (some) if statements. Others seem harmless, or even helpful, such as introducing parentheses around a literal tuple. Introducing parentheses around expressions after a print statement is dubious, given that I used python 2, not 3.
 #. Re-formatting expressions to introduce spaces around operators
 #. Reduction of a multi-line, triple-quoted string to a single-quoted string containing '\n' characters.
     This is unfortunate as this string is a few hundred lines long and contains the OMeta grammar. The reduction renders the grammar effectively unreadable.

Most of the above issues seem to be matters of opinion and should be deferred to `PEP 8 <http://www.python.org/dev/peps/pep-0008/>`_. This unparser's effects seem very similar to :ref:`those of Python's unparser <python_unparser_output>`.


Pepping
^^^^^^^

Conclusion
^^^^^^^^^^

This is not a test of Python-Decompiler, just an indication of where some of its strengths/weaknesses may lie.
