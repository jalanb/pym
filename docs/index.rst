.. pym documentation master file, created by
   sphinx-quickstart on Mon Dec 24 01:47:53 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _pym_index:

pym v0.1.5 documentation
========================

What is pym?
------------

Python code to code structures.

pym was inspired by vim but it handles structured (not plain) text. At present pym is entirely vapourware, and consists of some ideas based around :ref:`mindful_manipulation` of `Abstract Syntax Trees <http://en.wikipedia.org/wiki/Abstract_syntax_tree>`_, such as those provided by the `ast module <http://docs.python.org/2/library/ast.html?highlight=ast>`_ .

Parsing
^^^^^^^

:ref:`parsing` is interesting, as a means of transforming plain to structured text. :ref:`renderers` is the opposite of parsing, and transforms structured to plain text.

pym treats parsing and rendering as separate operations, but ideally they should be a single, reversible process. They will provide a "back end" to pym, connecting stored text, which is plain, to structured text which can be edited.

Editing
^^^^^^^

Editing is the heart of pym, a means of transforming ideas into structured text.

An editor is an interface between a person and structured text. The person has a keyboard and sees a window, hitting keys changes the window. The person first needs to learn which keys lead to which changes on screen.

I have a screen, you have a keyboard. I have code (and stuff) that I could show you, you have the means to choose between them. Assuming your capacity for choosing is infinite, so I need to know which code you'd like to look at. So we'll start with disk structures - trees with directories and files. And some recognisable patterns. Sounds like a similar structure to real code (modules are trees with blocks and lines), but simpler.

Structured text is ever a snapshot from a flow of ideas the coder has about the program being created. On a good day the ideas flow toward some runnable tree which works, but on a bad day they `chase around random forests <https://en.wikipedia.org/wiki/Mind_monkey>`_, crashing blindly into `insects <https://en.wikipedia.org/wiki/Software_bug>`_. It is important to store correct program text, more important to grasp ideas behind that text, and most important to grok the flow.

An editor should be the first step of a `REPL <https://en.wikipedia.org/wiki/REPL>`_: reading ideas from the coder and passing them on to an evaluator, and incidentally to a disk. It is rarely an end in itself, and should not get in the way of the larger cycle. Hence an editor should be quick, and more efficient of the coder's time than other factors. pym should look for the flow of ideas in the iterations of the REPL, noting steps such as when tests start to pass, and so development moves on.

pym should be editable by itself. This is a high priority - I do not have a lot of time for coding personal projects such as pym, the sooner it is "good enough" to be usable daily for editing other programs, but *quickly* fixable, then the more development it will actually get. (Such has been my experience with `my dot files <https://github.com/jalanb/dotjab/blob/master/functons>`_, in particular since I added `we <https://github.com/jalanb/what/blob/650677f8d0e80bc9aa9552cb5f87c42d34801b30/what.sh#L55>`_).

pym is inherently a modal editor, and one is not directly editing plain text. Some parts of the program will look more like plain text than others, e.g. names. But each structure in the tree uses its own specialised sub-editor, e.g. there is a different editor for an else branch than for a function definition than for a function. pym should transition between such editors unnoticeably to the user, not needing any "start loop here" instructions, although they could be explicitly given. Command/insert mode might toggle on the CAPS LOCK key.

pym is UI agnostic, capable of presentation between pipes, on a console, GUI, web page, or directly from Python. Development shall concentrate on Python first, console second, with others trailing. Full use should be made of available visual cues, such as colour, position, movement, ...

The user should be presented with program objects (e.g. projects, methods, operators) first and incidentals (e.g. files) second, if at all.

Programs
--------

A program is a history of a flow of ideas into a structured text representing a working algorithm.

Those ideas are *intentions* - what the coder wants to happen at run time.

Indices and tables
==================

Parts of the documentation:

.. toctree::
   :maxdepth: 2

   parsing
   renderers
   miscellaneous

* :ref:`genindex`
* :ref:`search`

