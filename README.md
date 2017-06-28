pym (deprecated)
================

pym was going to help with "editing code, not text.

No Java neither."

home
----
Main repo was on [GitHub](https://github.com/jalanb/pym), but the good stuff is on [ReadTheDocs](https://pym.readthedocs.io). (Wonder if there's a blog in it?)

So, like the man said, "bye for now, and thanks for all the fish"

Documentation
=============

pym remained almost entirely vapourware at it's end, but has [working code](https://github.com/jalanb/pym/tree/master/pym) to [parse](https://github.com/jalanb/pym/tree/master/pym/ast) [python](https://github.com/jalanb/pym/blob/master/pym/ast/parse.py#L4) and [bash](https://github.com/jalanb/pym/tree/master/pym/grammars) to [noramlised ASTs](https://github.com/jalanb/pym/blob/master/pym/ast/nst.py#L42), then [transform](https://github.com/jalanb/pym/tree/master/pym/ast/transform), [render](https://github.com/jalanb/pym/tree/master/pym/render) and [edit](https://github.com/jalanb/pym/blob/master/pym/edit/tree.py#L100) NSTs, with some [late night inspirations](https://github.com/jalanb/pym/blob/master/pym/edit/up_goer_five_for_jira.py) added for "good measure".

The coder wants to edit structural entitites (e.g. modules, methods, mocks), not incidentals (e.g. text, files).

The coder doesn't want to write anything at all, they should only need to choose their favourite cliches, algorithms, functions, packages, ...

Travis
------
[![Build Status](https://travis-ci.org/jalanb/pym.svg?branch=v0.1.3)](https://travis-ci.org/jalanb/pym)
