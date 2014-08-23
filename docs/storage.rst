.. pym documentation about storing text
    created by jalanb on Friday 22nd August 2014

.. _storage:

Text Storage
============

Text should be stored plainly, to fit it with existing tools and paradigms, and to leverage as much of the coder's existing habits as posible.

  I, and the programming community in general, have too long and deep a committment to programs stored as plain text to allow an easy transition beyond that.

  Moving to a structured store of programs would also require re-creation of the vast environment of plain-text based tools, e.g. grep, gcc and git. Other projects are `taking on <http://peaker.github.io/lamdu/>`_ such tasks, but my inclination is towards the Unix philosophy of doing one thing well, and to pipe from stdin to stdout.

Text is always a current snapshot, so storage should be to a VCS rather than simple disk.

Storage is always needed, and should be implict, without user intervention.
