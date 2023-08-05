Changelog
=========

1.0b2 (2018-11-09)
------------------

- Change option to ``folder`` as package.json is expected to be there, i.e.

::

    [yarn.build]
    folder = path/to/folder/

1.0b1.post0 (2018-11-09)
------------------------

- Fix (hopefully), pypi rendering.

1.0b1 (2018-11-09)
------------------

- Allow to configure where package.json is located via a setup.cfg section:

::

    [yarn.build]
    file = path-to/package.json

1.0a6 (2017-01-06)
------------------
- Create universal wheels again.

1.0a5 (2017-01-06)
------------------
- Pass the parent folder where package.json is.

1.0a4 (2017-01-06)
------------------
- Typos are fun...

1.0a3 (2017-01-06)
------------------
- Ditch wheels by now, only source releases.

1.0a2 (2017-01-06)
------------------
- Be more verbose.

1.0a1 (2017-01-05)
------------------
- Initial release.
