.. pym documentation master file, created by
   sphinx-quickstart on Mon Dec 24 01:47:53 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _pym_index:

.. raw:: html

    <style> .red {color:red} </style>
    <style> .blue {color:blue} </style>
    <style> .green {color:green} </style>

pym v0.1.7 documentation
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

An editor is an interface between a person and structured text. The person has a keyboard and sees a window, tapping keys changes the window. The person first needs to learn which keys lead to which changes on screen. As soon as changes are made the screen shows diff from original.

Screen shows one dir, file or function (aka package, module or function) at a time.

We are stopped on a breakpoint, showing a function, with stopped line underlined in :red:`red`. If there is an active error (aka Exception) then all (all data leading to) data on this line is marked :red:`red`. All code which has been run without error is shown :green:`green`, and all other data is shown :blue:`blue`.

18 Keys: j/k (up/down (+/- Y)), h/l (backward/forward (-/+ X)), g/; (out/in (-/+ Z))
      u/i (keyboard/screen), y/o (), t/p (take/paste)
      m/, (mark/goto), n/. (type/continue), b// (bookmark/search)

More leftward keys (on a QWERTY keyboard) "more general", "pull", "back"
More rightward keys mean "more specific", "push", "forward

Warning to vim users - some keys may seem the opposite of what you're used to.

What are we all doing here anyway?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

I have a screen, you have a keyboard.

I have codes, etc., that I could show you, you have the means to choose between them. Assuming your capacity for choosing is infinite, I need to know which code you'd like to look at. So we'll start with disk structures - trees with directories and files. And some recognisable patterns. Sounds like a similar structure to real code (modules are trees with blocks and lines), but simpler.

Structured text is ever a snapshot from a flow of your ideas to the codes being witten. On a good day the ideas flow toward some runnable tree which works, but on a bad day they `chase around random forests <https://en.wikipedia.org/wiki/Mind_monkey>`_, crashing blindly into `insects <https://en.wikipedia.org/wiki/Software_bug>`_. It is important to store correct program text, more important to grasp ideas behind that text, and most important to grok the flow.

An editor should appear in a `debugger <https://docs.python.org/3/library/pdb.html>`_: accepting `changes <>`_ from the coder and passing them on to an `evaluator<  >`_, and incidentally to a `disk <http://www.pygit2.org/>`_. It is rarely an end in itself, and should not get in the way of the larger cycle. Hence an editor should be quick, and more efficient of the coder's time than other factors. pym should look for the flow of ideas in the iterations of the REPL, noting steps such as when tests start to pass, and so development moves on.

pym should be editable by itself. This is a high priority - I do not have a lot of time for coding personal projects such as pym, the sooner it is "good enough" to be usable daily for editing other programs, but *quickly* fixable, then the more development it will actually get. (Such has been my experience with `my dot files <https://github.com/jalanb/dotjab/blob/master/functons>`_, in particular since I added `a function to edit functions <https://github.com/jalanb/what/blob/650677f8d0e80bc9aa9552cb5f87c42d34801b30/what.sh#L55>`_).

pym is inherently a modal editor, and one is not directly editing plain text. Some parts of the program will look more like plain text than others, e.g. names. But each structure in the tree uses its own specialised sub-editor, e.g. there is a different editor for an else branch than for a function definition than for a function. pym should transition between such editors unnoticeably to the user, not needing any "start loop here" instructions, although they could be explicitly given. Command/insert mode might toggle on the CAPS LOCK key.

pym is UI agnostic, capable of presentation between pipes, on a console, GUI, web page, or directly from Python. Development shall concentrate on Python first, console second, with others trailing. Full use should be made of available visual cues, such as colour, position, movement, ...

The user should be presented with program objects (e.g. projects, methods, operators) first and incidentals (e.g. files) second, if at all.

Programs
--------

A program is a history of a flow of ideas into a structured text representing a working algorithm.

Those ideas are *intentions* - what the coder wants to happen at run time.

Usage
-----

    $ pym main.py

or 

    $ pym main.sh



You are shown a line of code in a function. You can move around: (A subset of) vim keys work, with the slight catch the 'j'/'k' moves down/up the call stack, 'h'/'l' moves left/right along the block of statements, and 'g'/';' move out/in (through links to other code, e.g. function calls).

You can edit the code of the function, which will change the availability of run-time data.

Colours:

Errors shown in red, good code shown in green, links shown in blue. Untried code shown in white.

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

