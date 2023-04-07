pym (deprecated)
================

`pym` extends `python -m`

pym was going to help with "Editing code. Not text, no Java neither.", so there's a lot of that baggage still around.

install
-------

```
$ python -m pip install pym
```

Use
---

```
$ python -m pym
```
And then, e.g.
```
$ pym pip install requests
```

Side-effects
------------

`pym` may abuse your `python` installation, try in a `virtual environment` first
`pym` may really mess with your shell. Not recommended for `~/.bashrc`, yet

Old stuff
---------
The code stuff was on [GitHub](https://github.com/jalanb/pym), but the good stuff is on [ReadTheDocs](https://pym.readthedocs.io).

So, like the man said, "bye [for now](https://github.com/jalanb/pai/blob/master/README.md), and thanks for all the fish"

Documentation
=============

pym remained almost entirely vapourware at it's end, but has [working code](https://github.com/jalanb/pym/tree/master/pym) to [parse](https://github.com/jalanb/pym/tree/master/pym/ast) [python](https://github.com/jalanb/pym/blob/master/pym/ast/parse.py#L4) and [bash](https://github.com/jalanb/pym/tree/master/pym/grammars) to [noramlised ASTs](https://github.com/jalanb/pym/blob/master/pym/ast/nst.py#L42), then [transform](https://github.com/jalanb/pym/tree/master/pym/ast/transform), [render](https://github.com/jalanb/pym/tree/master/pym/render) and [edit](https://github.com/jalanb/pym/blob/master/pym/edit/tree.py#L100) NSTs.

The coder wants to edit structural entitites (e.g. modules, methods, mocks), not incidentals (e.g. text, files).

The coder doesn't want to write anything at all, they should only need to choose their favourite cliches, algorithms, functions, packages, ...

Travis
------
[![Build Status](https://travis-ci.org/jalanb/pym.svg?branch=v0.1.3)](https://travis-ci.org/jalanb/pym)
