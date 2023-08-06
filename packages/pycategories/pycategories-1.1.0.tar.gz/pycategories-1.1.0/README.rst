Pycategories
============

|master pipeline| |master coverage|

Pycategories is a Python 3 library that implements ideas from `category theory <https://en.wikipedia.org/wiki/Category_theory>`_, such as monoids, functors, and monads.  It provides a Haskell-influenced interface for defining instances of those typeclasses and defines several right out of the box, for example the Maybe monad:

::

   >>> from categories import apply
   >>> from categories.maybe import Just, Nothing
   >>> f = Just(lambda x: x ** 2)
   >>> x = Just(17)
   >>> apply(f, x)
   Just(289)
   >>> apply(f, Nothing())
   Nothing

Or to define your own instance of a typeclass:

::

   >>> from categories import mappend, mempty, monoid
   >>> monoid.instance(dict, lambda: {}, lambda a, b: dict(**a, **b))
   >>> mappend({'foo': 'bar'}, {'rhu': 'barb'})
   {'foo': 'bar', 'rhu': 'barb'}


Installation
------------

::

   pip install pycategories


To clone the repo and install dependencies for development: ::

  git clone https://gitlab.com/danielhones/pycategories
  cd pycategories
  pip install -e .[dev]


Support and Contributing
------------------------

* `Issue Tracker <https://gitlab.com/danielhones/pycategories/issues>`_
* `Source code <https://gitlab.com/danielhones/pycategories>`_
* `Contributing Guide <https://gitlab.com/danielhones/pycategories/blob/master/CONTRIBUTING.rst>`_


License
-------

Pycategories is licensed under the `MIT License <https://gitlab.com/danielhones/pycategories/blob/master/LICENSE>`_


Documentation
-------------

Documentation is available at `pycategories.readthedocs.io <http://pycategories.readthedocs.io/>`_


.. |master pipeline| image:: https://gitlab.com/danielhones/pycategories/badges/master/pipeline.svg
   :target: https://gitlab.com/danielhones/pycategories/commits/master
.. |master coverage| image:: https://gitlab.com/danielhones/pycategories/badges/master/coverage.svg
   :target: https://gitlab.com/danielhones/pycategories/commits/master
