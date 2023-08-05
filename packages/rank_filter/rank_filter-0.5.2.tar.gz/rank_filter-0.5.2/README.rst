|Travis Build Status| |License| |PyPI Release| |conda-forge Release| |Gitter|

--------------

Rank Filter
===========

Motivation
----------

This package is designed to provide an efficient linear rank order
filter written in C++ with Python bindings. It can take single or double
precision floats as input. It was needed as the equivalent percentile
filter in SciPy was found to be too slow and unnecessarily general.
There was no equivalent in VIGRA.

Requirements
------------

In order to build this package, the following requirements are needed.

1. Python (2.7.x or 3.5.x)
2. Boost (1.56.0 or later)
3. NumPy (1.7.0 or later)
4. Cython (0.23.0 or later)
5. Setuptools (18.0 or later)

Installation
------------

The easiest way to install is to install our ``conda`` package.
Alternatively, one can install from ``pip``, but this will require a
C++ compiler and a recent version of ``setuptools``.

Building
--------

There are several ways to build the package.

1. Standard Python build and install.
2. Conda recipe build and install.
3. CMake build and install.

The vanilla install in any of these forms should be basically equivalent.

Getting Started
~~~~~~~~~~~~~~~

To start simply clone the repo and change directory to the repo.

::

    git clone https://github.com/nanshe-org/rank_filter
    cd rank_filter

Using Python
~~~~~~~~~~~~

To build/install with Python directly, simply run the following command.

::

    python setup.py install

Using Conda
~~~~~~~~~~~~

To build/install with Conda, simply run the following command.

::

    conda build rank_filter.recipe
    conda install --use-local rank_filter.

Using CMake
~~~~~~~~~~~

In order to find Boost includes and libraries, the directory Boost was installed
to must be set as ``BOOST_ROOT``.

::

    cmake -DBOOST_ROOT=<path-to-Boost-root> .


Also the CMake installer will also pick these variables up if they are set in
the environment and not provided.

::

    export BOOST_ROOT=<path-to-Boost-root>
    cmake .

Additionally, the preferred python interpreter can be set by using the
``PYTHON_EXECUTABLE`` variable.

Checking
********

Before building the Python bindings it is worth checking if the C++ code
passes its own test suite. This can be done using ``make`` with the
command below. It is not required to run this stage, but it will be run
every time when building. These test are no guarantee that the Python
module will work. All they verify is that the C++ code works.

::

    make check

Building
********

Building is done easily using ``make``. This will create a shared object
in the slib directory, which can be imported by Python as a module. As
mentioned in the Checking section, the C++ tests will be run first. If
they fail, the Python module will not be built. They do not guarantee
that the Python module will work. Instead the testing stage can be used
to validate the module.

::

    make

Testing
*******

Once the Python module is built, it is worth testing whether it works.
This can be done with ``make`` using the command below. Unlike the C++
tests, these are Python tests that use nose to run the tests. The tests
are the Python analogues of the ones used in C++ tests. They not only
verify that basic command run, but that they pass with correct results
only.

::

    make test

Installing
**********

After building and testing, it is time to install. Using ``make``, the
command below will install the module in the identified Python's
site-package folder allowing for importing this module using that
Python.

::

    make install

Cleaning
********

There are a few additional options regarding cleaning. It is possible to
clean all build intermediates (including CMake generated files) leaving
only the final build products. This is done by calling as below.

::

    make distclean

If it is desirable to eliminate the build products as well as all
intermediates, then the call below can be used.

::

    make reset


.. |Travis Build Status| image:: https://travis-ci.org/nanshe-org/rank_filter.svg?branch=master
   :target: https://travis-ci.org/nanshe-org/rank_filter

.. |License| image:: https://img.shields.io/badge/license-BSD%203--Clause-blue.svg
   :target: https://raw.githubusercontent.com/nanshe-org/rank_filter/master/LICENSE.txt

.. |PyPI Release| image:: https://img.shields.io/pypi/v/rank_filter.svg
   :target: https://pypi.python.org/pypi/rank_filter

.. |conda-forge Release| image:: https://img.shields.io/conda/vn/conda-forge/rank_filter.svg
   :target: https://anaconda.org/conda-forge/rank_filter

.. |Gitter| image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/nanshe-org/rank_filter
   :target: https://gitter.im/nanshe-org/rank_filter?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
