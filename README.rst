pl-mgz2imgslices
================================

.. image:: https://badge.fury.io/py/mgz2imgslices.svg
    :target: https://badge.fury.io/py/mgz2imgslices

.. image:: https://travis-ci.org/FNNDSC/mgz2imgslices.svg?branch=master
    :target: https://travis-ci.org/FNNDSC/mgz2imgslices

.. image:: https://img.shields.io/badge/python-3.5%2B-blue.svg
    :target: https://badge.fury.io/py/pl-mgz2imgslices

.. contents:: Table of Contents


Abstract
--------

An app to ...


Synopsis
--------

.. code::

    python mgz2imgslices.py                                           \
        [-v <level>] [--verbosity <level>]                          \
        [--version]                                                 \
        [--man]                                                     \
        [--meta]                                                    \
        <inputDir>
        <outputDir> 

Description
-----------

``mgz2imgslices.py`` is a ChRIS-based application that...

Arguments
---------

.. code::

    [-v <level>] [--verbosity <level>]
    Verbosity level for app. Not used currently.

    [--version]
    If specified, print version number. 
    
    [--man]
    If specified, print (this) man page.

    [--meta]
    If specified, print plugin meta data.


Run
----

This ``plugin`` can be run in two modes: natively as a python package or as a containerized docker image.

Using PyPI
~~~~~~~~~~

To run from PyPI, simply do a 

.. code:: bash

    pip install mgz2imgslices

and run with

.. code:: bash

    mgz2imgslices.py --man /tmp /tmp

to get inline help. The app should also understand being called with only two positional arguments

.. code:: bash

    mgz2imgslices.py /some/input/directory /destination/directory


Using ``docker run``
~~~~~~~~~~~~~~~~~~~~

To run using ``docker``, be sure to assign an "input" directory to ``/incoming`` and an output directory to ``/outgoing``. *Make sure that the* ``$(pwd)/out`` *directory is world writable!*

Now, prefix all calls with 

.. code:: bash

    docker run --rm -v $(pwd)/out:/outgoing                             \
            fnndsc/pl-mgz2imgslices mgz2imgslices.py                        \

Thus, getting inline help is:

.. code:: bash

    mkdir in out && chmod 777 out
    docker run --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
            fnndsc/pl-mgz2imgslices mgz2imgslices.py                        \
            --man                                                       \
            /incoming /outgoing

Examples
--------





