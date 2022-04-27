.. pym documentation master file, created by
   sphinx-quickstart on Mon Dec 24 01:47:53 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _pym_index:

.. raw:: html

    <style> .red {color:red} </style>
    <style> .blue {color:blue} </style>
    <style> .green {color:green} </style>

pym v0.3.3 documentation
========================

What is pym?
------------

`pym` helps with editing code, not text (:ref:`java_rst`).

`pym` knows what code is, from a programmer's point of view: controlled flow of structured data through semantically connected algorithms. 

Code is expressed in a language, such as `Python <https://github.com/jalanb/pym/blob/master/pym/ast/parse.py#L9>`_ or `Bash <https://github.com/jalanb/parsher/blob/master/parsher/__init__.py#L32>`_, `etc <https://pypi.python.org/pypi/grako/3.6.6#abstract-syntax-trees-asts>`_.

Code is parsed to an `Abstract Syntax <https://github.com/jalanb/pym/blob/master/pym/ast/nst.py#L88>`_, filtering out as many language specific details as possible. `pym`

which can be annotated with interesting properties and connections.

Such a connected  NST ("Normal Syntax Tree") links known names to known Syntax Trees. , and can catch any runtime problems, providing source for each stack frame.

`pym` was inspired by vim but it handles structured (not plain) text. At present `pym` is entirely vapourware, and consists of some ideas based around  `mindful <https://www.youtube.com/watch?v=92i5m3tV5XY>`_ manipulation of `Abstract Syntax Trees <http://en.wikipedia.org/wiki/Abstract_syntax_tree>`_, such as those provided by the `ast module <http://docs.python.org/2/library/ast.html?highlight=ast>`_ and `ZatSo <https://github.com/jalanb/ZatSo/blob/master/zatso/upgoers/readme.md>`_ . It would help  if the parser could handle `bash script <https://github.com/jalanb/parsher/blob/master/parsher/__init__.py#L9>`_ too.

Parsing
^^^^^^^

:ref:`parsing_page` should be more boring, but remains interesting, at least as a means of transforming plain to structured text. `Rendering <https://github.com/jalanb/pym/tree/master/pym/render>`_ is ! parsing.

`pym` treats parsing and rendering as separate operations, but ideally they should be a single, reversible process. They will provide a "back end" to `pym`, connecting stored text, which is plain, to structured text which `can be editted <https://github.com/jalanb/pym/blob/master/pym/edit/main.py#L41>`_.

Editing
^^^^^^^

`Editting <https://github.com/jalanb/pym/blob/master/pym/edit/main.py#L41>`_ is the heart of `pym`, a means of transforming ideas into structured text.

An editor is an interface between a person and structured text. The person has a keyboard and sees a window, tapping `keys <https://github.com/jalanb/pym/blob/master/pym/edit/keyboard.py#L35>`_ `changes <https://github.com/jalanb/pym/blob/master/pym/edit/main.py#L54>`_ the window. The person first needs to learn `which keys lead <https://github.com/jalanb/pym/blob/master/pym/edit/keyboard.py#L35>`_ to which `changes <https://github.com/jalanb/pym/blob/master/pym/edit/tree.py#L104>`_ on screen. As soon as changes are made the screen shows diff from original.

Screen shows one dir, file or function (aka package, module or function) at a time.

We are stopped on a breakpoint, showing a function, with stopped line underlined in red. If there is an active error (aka Exception) then all (data leading to) data on this line is marked red. All code which has been run without error is shown in green, and all other data is shown in blue.

18 Keys: j/k (up/down (+/- Y)), h/l (backward/forward (-/+ X)), g/; (out/in (-/+ Z))
      u/i (keyboard/screen), y/o (), t/p (take/paste)
      m/, (mark/goto), n/. (type/continue), b// (bookmark/search)

More leftward keys (on a QWERTY keyboard) "more general", "pull", "back"

More rightward keys mean "more specific", "push", "forward

Warning to vim users - some keys may seem the opposite of what you're used to.

What are we all doing here anyway?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

I have a screen, you have a keyboard.

I have `codes <https://github.com/jalanb/dotjab/tree/master/src>`_, `etc <https://github.com/jalanb/dotjab/tree/master/environ.d>`_., that I could `show <https://github.com/jalanb/pym/blob/master/pym/render/render.py#L19>`_ you, you have the means to `choose between them <https://github.com/jalanb/pym/blob/master/pym/edit/keyboard.py#L39>`_. Assuming your capacity for choosing is infinite, I need to know which `code you'd like to look at <https://github.com/jalanb/pym/blob/master/pym/ast/parse.py#L7>`_. So we'll start with `disk structures <https://github.com/jalanb/pym/blob/master/here_be_dragons/pyrception/pyrceive.py#L184>`_- trees with `directories <https://github.com/jalanb/pym/blob/master/pym/ast/nst.py#L11>`_ and `files <https://github.com/jalanb/pym/blob/master/pym/ast/nst.py#L15>`_. And some `recognisable patterns <http://bfy.tw/3igB>`_. Sounds like a similar structure to `real code <https://github.com/jalanb/pym/blob/master/pym/ast/lists.py#L25>`_ (modules are `trees <https://github.com/jalanb/pym/blob/master/pym/ast/nst.py#L5>`_  with blocks and `lines <https://github.com/jalanb/pym/blob/master/pym/ast/transform/reliner.py#L36>`_), but simpler. But you didn't hear that from me.

Anyway, structured text is ever a snapshot from a flow of your ideas to the codes being witten. On a good day the ideas flow toward some runnable tree which works, but on a bad day they `chase around random forests <https://en.wikipedia.org/wiki/Mind_monkey>`_, crashing blindly into `insects <https://en.wikipedia.org/wiki/Software_bug>`_. It is important to store correct program text, more important to grasp ideas behind that text, and most important to grok the flow.

An editor should appear in a `debugger <https://docs.python.org/3/library/pdb.html>`_: accepting `changes <>`_ from the coder and passing them on to an `evaluator<  >`_, and incidentally to a `disk <http://www.pygit2.org/>`_. An editor is rarely an end in itself, and should not get in the way of the larger cycle. Hence an editor should be quick, and more efficient of the coder's time than other factors.

`pym` should look for the flow of ideas in the iterations of the REPL, noting steps such as when tests start to pass, and so development moves on.

`pym` should be editable by itself. This is a **high priority** - I do not have a lot of time for coding personal projects such as `pym`, the sooner it is "good enough" to be usable daily for editing other programs, but *quickly* fixable, then the more development it will actually get. (Such has been my experience with `my dot files <https://github.com/jalanb/dotjab/blob/master/functons>`_, in particular since I added `a function to edit functions <https://github.com/jalanb/what/blob/650677f8d0e80bc9aa9552cb5f87c42d34801b30/what.sh#L55>`_).

Modality
^^^^^^^^

`pym` is inherently a modal editor, and one is not directly editing plain text. Some parts of the program will look more like plain text than others, e.g. names. But each structure in the tree uses its own specialised sub-editor, e.g. there is a different editor for an else branch than for a function definition than for a function. `pym` should transition between such editors unnoticeably to the user, not needing any "start loop here" instructions, although they could be explicitly given.

Command/insert mode might toggle on the CAPS LOCK key. `pym` is UI agnostic, capable of presentation between pipes, on a console, GUI, web page, or directly from Python. Development shall concentrate on Python first, console second, with others trailing. Full use should be made of available visual cues, such as colour, position, movement, ...

The user should be presented with program objects (e.g. projects, methods, operators) first and incidentals (e.g. files) second, if at all.

Programs
--------

A program is a history of a flow of ideas into a structured text representing a working algorithm.

Those ideas are *intentions* - what the coder wants to happen at run time.

Usage
-----
To run the installed package called kat
```
    $ python -m kat -h
```
or 
```
    $ pym kat -h
```
or 
```
    $ python -m pym -m kat -h
```

They'll all show kat's help page


Vaporware
---------
```
    $ pym main.sh
```


Suddenly
--------

You are shown a line of code in a function.

You can move around, a subset of) vim keys work glitchily:
* `j`/`k` moves down/up the call stack,
* `h`/`l` moves left/right along the block of statements, and
* `g`/`;` move out/in (through links to other code, e.g. function calls).

You can edit the code of the function, which might change colours.

Colours:

* White: untried code
* Red: Errors
* Green: good code
* Blue: links

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

