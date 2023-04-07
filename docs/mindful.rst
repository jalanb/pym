.. pym documentation about mindful manipulation
    created by jalanb on Thursday 9th May 2013

.. _mindful_manipulation:

Manipulating text
=================

As an editor pym should allow manipulation of (structured) text. It should allow change of any changes, hence should work at the level of a user's *intentions*, not their mere edits.
 
.. toctree::
   :maxdepth: 1

Capturing Intentions
--------------------

I take it as a given that all changes to text should be considered temporary, because today's change will itself be changed tomorrow. And tomorrow's change will be easier if I know *why* today's change was made.

Most editors ignore this, because they handle text directly, and the user only indirectly. And so the reasons behind a change are invisible, and text becomes brittle because tomorrow I become wary of losing the original reason for today's change. Consider a simple `change from yesterday <https://github.com/jalanb/dotjab/commit/a60447db525a7fb9995fdd6f979a033e44460c85>`_::

    colour = priority_colour(item.priority)
    print colours.colour_text(colour, item.text)

If I want to change that code, say by removing the variable colour, I need to know firstly whether that variable is used later on in the code (or even: somewhere else in this file, this project, my code, someone else's code). The text in front of me is no help, but `the commit comment <https://github.com/jalanb/dotjab/commit/a60447db525a7fb9995fdd6f979a033e44460c85>`_ is.

And when I do know that I can make the change an ordinary editor will force me to 

 * goto "colour" on first line and delete, delete, delete, delete, delete, delete, delete, delete, delete.
 * copy the rest of the line
 * goto the comma on the second line (down, right, right, ..., right) and delete, delete, ..., delete.
 * paste

A better editor, like vim will make that a bit easier by allowing me to delete words instead of mere characters and quickly find the next "colour", but will still insist on 4 distinct operations.

But it is really one operation: "remove the variable", for only one reason: it was used as a debugging aid and is no longer needed.

Mindful Manipulation
--------------------

In order to capture such intentions one needs to stop thinking in terms of text, to move "up a level" by noticing why I'm doing "delete, delete, ..., delete". I need to notice these actions more consciously, hence mindful manipulation.

Separation of Concerns
----------------------

I notice an interesting extract from Chris Reade's book *Elements of Functional Programming* on `Wikipedia <https://en.wikipedia.org/wiki/Separation_of_concerns#Origin>`_:

    The programmer is having to do several things at the same time, namely,

    1. describe what is to be computed;

    2. organise the computation sequencing into small steps;

    3. organise memory management during the computation.

Reade continues to say,

    Ideally, the programmer should be able to concentrate on the first of the three tasks (describing what is to be computed) without being distracted by the other two, more administrative, tasks. Clearly, administration is important but by separating it from the main task we are likely to get more reliable results and we can ease the programming problem by automating much of the administration.

    The separation of concerns has other advantages as well. For example, program proving becomes much more feasible when details of sequencing and memory management are absent from the program. Furthermore, descriptions of what is to be computed should be free of such detailed step-by-step descriptions of how to do it if they are to be evaluated with different machine architectures. Sequences of small changes to a data object held in a store may be an inappropriate description of how to compute something when a highly parallel machine is being used with thousands of processors distributed throughout the machine and local rather than global storage facilities.

    Automating the administrative aspects means that the language implementor has to deal with them, but he/she has far more opportunity to make use of very different computation mechanisms with different machine architectures.

