"""
Python has many template languages and most Python developers have
used several or written their own (I'm guilty, Cheetah).  Very few
Python web developers use Python itself for HTML/view generation.
It's argued that template languages, compared to Python:

  a) provide better separation between domain model / application
     logic code and the presentation layer

  b) are easier to read and less prone to spaghetti code, as Python's
     built-in string interpolation/concatenation tools aren't well
     suited for HTML generation.

  c) make it easier to handle HTML escaping and character encoding
     correctly

  d) solve work-flow issues when collaborating with non-programmers
     (designers, writers, translators, etc.) who understand neither
     Python nor the tools required to work with it (editor, etc.).

  e) can provide a sandbox that insulates you from the mistakes or
     malicious code injections of unskilled or untrusted contributors
     (non-programmers, junior developers, contractors, etc.).

I used to believe these arguments but recently I've come to see them
as mostly dogma. Consider the example code in this module as evidence
for my counterargument:

It is easy to generate correct HTML from plain Python without a)
blurring the separation between the domain/application and
presentation layers, b) creating spaghetti code (HTML fragments
embedded in strings, a mess of str concats, etc.), or c) screwing up
the HTML-escaping.  Furthermore, there are big advantages to doing so:

  1) Full tool-chain support:
     - editor support: syntax highlighting, code nav tools,
       auto-completion, intellisense/eldoc, snippets, refactoring &
       search/replace tools, etc.
     - static code analyzers: pyflakes, pylint (especially with
       flymake in Emacs, or the equivalent in other editors, which
       highlights syntax errors and undefined variables as you type)
     - debuggers
     - testing/coverage tools: pycoverage, etc.

     Tool-chain support for template languages is patchy at best.  Even
     if it were perfect, it's yet another thing to learn, configure
     and maintain.

     Finally, the Python interpreter itself understands the code,
     unlike template src that is just an opaque string to it.  In fact
     with the example shown in this module, Python 'understands' far
     more about what you are doing than any template language can.
     The HTML in template src code is just an opaque string to a
     template parser, unless the parser is an XML parser and your
     template syntax is valid XML.

  2) Python is extremely expressive and requires far fewer keystrokes
     to output HTML than a template lang.  This is especially true of
     Django templates and its restrictive syntax and system of custom
     template tags.

  3) Good Python tools for view generation can support higher levels
     of abstraction and more declarative, 'intentional' coding styles
     than possible in templates, which are usually quite imperative.
     This can result in a more flexible, more readable, more testable
     and more reusable presentation layer.  This module attempts to
     achieve that by encouraging a strong separation between the
     declaration of a view and the definition of how it will be
     serialized.  See the final example.

  4) The implementation of a pure-Python view generator is far easier
     to grok, debug, and maintain than a template language
     implementation.  There's no lexer, parser, compiler /
     code-generator, or interpreter involved.  The core of this module
     is less than 250 sloc according to sloccount, while Django
     templates has roughly 2700, Cheetah's core is about 4000 sloc,
     Mako is also 4000, and Jinja2 seems to be almost 6000 (excluding
     the test suite).

My rebuttal to argument (d) (work-flow) is YAGNI!  The vast majority
of people writing templates are developers.  Designers usually
contribute mockups or css.  The rare designers who do actually work
with templates are fully capable of learning a subset of Python,
especially when it's less complicated than the template language
syntax.

Anyone who buys argument (e) (sandboxing and gentle error handling) is
living in the past by assuming that server-side domain code is somehow
more important than the presentation layer or what happens on the
browser and that it should be held to a higher standard.  A bug is a
bug.  These days, mistyped template variable names, incorrect
HTML/Javascript, missing or incorrect parts of the UI are just as
unacceptable as bugs or syntax errors in the back-end.  They should be
detected and handled early. Presentation layer code is just as
important as the back-end and should be held to the same standards.
Furthermore, if someone can include Javascript in the template there
is no sandboxing.  The same people I've heard using this argument are
also advocates of code-review, so I'm confused by their logic.

The basic usage work-flow for this module is:

1) Use Python to build a tree of objects (HTML elements, standard python
   types, your own types, whatever ...) that needs to be serialized into
   HTML.
   e.g.: tree = [doctype,
                 html[head[meta(charset='UTF-8')],
                      body[div[u'content', more_content_from_a_py_var]]]]

2) Build a `VisitorMap` that declares how each `type` should be
   serialized, or use an existing one.

3) Serialize the tree via a serialize function like this:
  def serialize(tree, visitor_map=default_visitors_map,
                input_encoding='utf-8'):
      return Serializer(visitor_map, input_encoding).serialize(tree)
      # returns unicode

  or in a WSGI context:

  def serialize(tree, wsgi_env):
      return Serializer(
          visitor_map=get_visitor_map(wsgi_env),
          input_encoding=get_input_encoding(wsgi_env)
          ).serialize(tree).encode(get_output_encoding(wsgi_env))

  The `tree` argument here doesn't have to be an HTML element.  It can be
  any Python type for which the visitor_map has a visitor.

This module is written in a semi-literate style and its code is
intended to be read:

Table Of Contents
  Part I: The Core
  1: str/unicode wrappers used to prevent double-escaping.
  2: Serializer class (a tree walker that uses the visitor pattern to
     serialize what it walks into properly escaped unicode)
  3: VisitorMap (a dict subclass that maps Python types to visitors)
  4: Default serialization visitors for standard python types

  Part II: Frosting
  5: Declarative classes for creating a DOM-like tree of XML/HTML
  6: Visitors for the XML/HTML elements, etc.

  Part III: Examples
  7: Helpers for examples
  8: Basic examples
  9: Extended example using some fictional model data

The tag syntax in sections 5 to 9 comes from Donovan Preston's 'Stan'
(part of Twisted / Nevow) and Cliff Wells' 'Brevé'.  If you don't like
it, please just remember my main argument and use your imagination to
dream up something better.  Lisp / scheme programmers are using
similar embedded DSLs for HTML-generation.  S-expressions and the
code-as-data / data-as-code philosophy make such a style very natural
in Lisps.  My argument and this code are an echo of what Stan, Brevé
and various lisp libraries have been doing for a long time.  (see
http://www.kieranholland.com/code/documentation/nevow-stan/
http://breve.twisty-industries.com/ and
http://article.gmane.org/gmane.lisp.scheme.plt/16412)

I find this `visitor pattern` variation much more interesting than this
particular tree building syntax.  Kudos to Python's dynamic, yet
strong and introspectable type system for enabling it.  It can be used
with other tree building styles or even to serialize to output formats
other than XML/HTML.  It is especially interesting when combined with
concepts from context-oriented programming and lean-programming.  If
you defer as many rendering choices as possible to the visitors and
visitor_map (lean programming's 'decide as late as possible') you gain
the ability to radically alter the view based on the current context
(think WSGI request environment), without having to change your view
declarations. Because visitors are registered per Python type rather
than per page / template, you have very fine-grained control. For
example, you can register visitors that are appropriate for the
current user's locale (for numbers, dates, times, images,
lazy-gettext-strings, etc), visitors that are appropriate for the
current user's permission levels or preferences, and visitors that
present extra information in design-mode or debug-mode.

If the approach in this module interests you, you may be interested in
my Cython/Pyrex optimized version. This pure Python version is roughly
twice as fast as Django templates.  The Cython version is 20 to 30
times faster than Django depending on usage: on par with Cheetah and
Mako.  The Cython version comes with full unit tests and a little
benchmark suite.  I'll be releasing it under the BSD license on
bitbucket and PyPI sometime before April 2010.  I have been using it
in production for the past 3 years.  However, I haven't chosen a name
for it yet.  If you have any suggestions, please share them with me.

There are a few uses cases where I still use and appreciate templates:
  - when composing a set of pages that contain lots of text
    sprinkled with the occasional variable and light markup

  - when composing email templates

Another option for these use cases is to put any large text blocks in
module level constants (to avoid having strange indentation) and use
Markdown, Textile, ReST, or something similar to handle the markup
prior to labeling them as `safe_unicode` (see below) that doesn't need
any further escaping.

p.s. I discovered after writing this that Cliff Wells wrote a similar
rant back in 2007:  http://www.enemyofthestatement.com/post/by_tag/29

p.p.s Christopher Lenz wrote a good reply to Cliff's post:

    In the end, the reason why I personally wouldn't use something like
    Stan or Breve is because I actually want to work directly with the
    HTML, CSS, and Javascript in my application. I want my text editor
    of choice  to be able to assist me with all the tools it provides
    for working with markup, including support for embedded CSS and
    Javascript. I want to be able to quickly preview a template by
    opening it directly in the browser, without having to run it
    through the template engine first. When I'm working on a template,
    I want to be using HTML, not  Python.
    -- http://www.cmlenz.net/archives/2007/01/genshi-smells-like-php

"""
