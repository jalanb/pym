.. pym documentation about Cenk Alti's pyhtml, created by
   jalanb on Monday Sptember 2nd, 2013

.. _pyhtml:

Cenk Alti's pyhtml
============================

pyhtml is a project by `Cenk Alti <http://http://cenkalti.net//>`_ which can render html from python sequences. Such sequences can look very similar to the generated html. Which is far more easily seen in `his example <https://pypi.python.org/pypi/PyHTML#example>`_, than in my explanation.

.. _jorges_pyhtml:

Links to pyhtml
---------------

* The source of the project is stored `on github <https://github.com/llou/pyhtml>`_.
* It is available `in the Cheeseshop <https://pypi.python.org/pypi/PyHTML>`_.

The code is `licensed under the Apache License, Version 2.0 <https://github.com/cenkalti/pyhtml/blob/master/LICENSE>`_, and so can be copied for investigation.

Summary
-------

pyhtml has been tested by Cenk with Python 2.7 only.


Rendering
---------

Running
^^^^^^^

I have run pythtml's tests with Pythons 2.5, 2.6 and 2.7. It passed with the latter only, but fails were only due to use of `assertIs <http://docs.python.org/2/library/unittest.html?highlight=assertis#unittest.TestCase.assertIs>`_ and `assertIn <http://docs.python.org/2/library/unittest.html?highlight=assertis#unittest.TestCase.assertIn>`_, both of which were introduced to `the unittest module <http://docs.python.org/2/library/unittest.html>`_ in 2.7. `Replacing them <https://github.com/jalanb/pyhtml/commit/e02264de5e9ded36647aeeed70098e0c44f786d7>`_ with the older `assertTrue <http://docs.python.org/2/library/unittest.html?highlight=assertis#unittest.TestCase.assertTrue>`_ led to the test suite passing in all three Python versions.


Conclusion
^^^^^^^^^^

