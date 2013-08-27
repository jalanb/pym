.. pym documentation about Alex Michael's approach, created by
   jalanb on Wednesday August 21st 2013

.. _approach:

Alex Michael's approach
==================================

approach is a project by `Alex Michael <http://alexmic.net/>`_ as a "toy" example of an HTML template engine.

.. _eduardos_approach:

Links to approach
-----------------------

  * The approach project is explained at `Alex's website <http://alexmic.net/building-a-template-engine/>`_ only.

Summary
-------

approach is more a teaching tool than intended for production use. As such it is a good exemplar for the many Python tools which render HTML from templates, which include some embedded Python.

 It parses templates, which are html with included python snippets, to produce an AST, and then renders the AST to HTML. The AST is represented by an object per node, with the objects being instantiations of Node subclass. Each subclass has its own version of a ``render()`` method, to which is provided a context. Such a class can also include supporting code to help with the rendering of the HTML, and so can be `more than a simple rendering <https://github.com/alexmic/microtemplates/blob/master/microtemplates/base.py#l155>`_.

It is released without any license, so cannot be copied.
