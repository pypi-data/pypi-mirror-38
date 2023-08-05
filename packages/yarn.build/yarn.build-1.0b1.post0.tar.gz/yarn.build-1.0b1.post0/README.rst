Introduction
============
This package builds JavaScript projects with `yarn`_.
It contains a `zest.releaser`_ entry point and a stand-alone command line tool.

Goal
====
You want to release a package that has a ``packages.json`` on it and a ``release`` script defined on it.

Usually one does not want to keep the generated files on VCS,
but you want them when releasing with `zest.releaser`_.

Credits
=======
This package is a direct inspiration from `zest.pocompile`_ from Maurits van Rees.

Thanks!

To Do
=====
Add tests

.. _`yarn`: https://yarnpkg.com/
.. _`zest.releaser`: http://pypi.python.org/pypi/zest.releaser
.. _`zest.pocompile`: http://pypi.python.org/pypi/zest.pocompile
