.. image:: https://travis-ci.org/G-Node/nixpy.svg?branch=v1.4
    :target: https://travis-ci.org/G-Node/nixpy
.. image:: https://ci.appveyor.com/api/projects/status/nrsgupr9ura3vli3/branch/v1.4?svg=true
    :target: https://ci.appveyor.com/project/achilleas-k/nixpy-um2sy/branch/v1.4
.. image:: https://coveralls.io/repos/github/G-Node/nixpy/badge.svg?branch=v1.4
    :target: https://coveralls.io/github/G-Node/nixpy?branch=v1.4


----

About NIXPY
-----------

The *NIXPY* project is an extension to `NIX <https://github.com/G-Node/nix>`_ and provides Python bindings for *NIX*.

Getting Started
---------------

The simplest way to install *NIXPY* is from PyPI using pip. The name of the package is nixio_::

    pip install nixio

Bindings for C++ NIX
--------------------

The setup script will automatically build the bindings for *NIX* if it is detected on the system, otherwise only the pure Python version will be installed.

For instructions on building *NIX*, see the `NIX README <https://github.com/G-Node/nix/blob/master/README.md>`_ file.


To check if installed properly
------------------------------

Try importing nixio::

    >>> import nixio
    >>>

If python successfully executes :code:`import nixio`, the installation went well.
Check out the API documentation for further tutorials.


NIXPY API Documentation
-----------------------

The API documentation can be found `here <http://g-node.github.io/nixpy/>`_.


.. _nixio: https://pypi.python.org/pypi/nixio
