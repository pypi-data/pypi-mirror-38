ghx
###

Run scripts from GitHub, `npx`_-style.

.. _npx: https://www.npmjs.com/package/npx


Usage
=====

::

    ghx rshk/ghx-example

In its most basic form, it will make a shallow copy of the specified
GitHub repository and run a script from it.

By default, it will look for an executable named ``bin/run`` inside
the repo folder.


Run a different script::

  ghx rshk/ghx-example/bin/two


Or from a different branch::

  ghx -b foobar rshk/ghx-example


Installation
============

You need a Python 3 interpreter and pip installed.

::

    pip install ghx

Or install in the user home directory (usually ``~/.local``)::

  pip install --user ghx

(Make sure you have ``~/.local/bin`` in your ``PATH``)
