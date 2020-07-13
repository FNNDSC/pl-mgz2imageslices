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

A ChRIS pulgin to convert ``.mgz`` files to readable formats like PNGs or JPEGs.


Synopsis
--------

.. code::

    python mgz2imgslices.py                                         \
            [-i] [--inputFile] <inputFile>                              \
            [-o] [--outputFileStem] <outputFileStem>                    \
            [-t] [--outputFileType] <outputFileType>                    \
            [-n] [--normalize]                                          \
            [-l] [--lookuptable] <LUTcolumnToNameDirectories>           \
            [-s] [--skipLabelValueList] <ListOfLabelNumbersToSkip>      \
            [-h] [--help]                                               \
            [--json]                                                    \
            [--man]                                                     \
            [--meta]                                                    \
            [--savejson <DIR>]                                          \
            [-v <level>] [--verbosity <level>]                          \
            [--version]                                                 \
            [-y] [--synopsis]                                           \
            <inputDir>                                                  \
            <outputDir>  

Description
-----------

``mgz2imgslices.py`` is a ChRIS-based application that convert ``.mgz`` files to readable formats like PNGs or JPEGs.

It bifurcates all the labels within a ``.mgz`` file and stores all the slices corresponding to each label within individual directories named after the label number. 

**NOTE:** 

Labels represent the different cortical segments of the brain. 
Refer to the file: ``FreeSurferColorLUT.txt`` in this repository for names and IDs of all the labels that a ``.mgz`` can have.  

Arguments
---------

.. code::

    [-i] [--inputFile] <inputFile>
    Input file to convert. Should be a .mgz file

    [-o] [--outputFileStem] <outputFileStem>
    The output file stem to store conversion. If this is specified
    with an extension, this extension will be used to specify the
    output file type.

    [-t] [--outputFileType] <outputFileType>
    The output file type. If different to <outputFileStem> extension,
    will override extension in favour of <outputFileType>. Should be a 'png' or 'jpg'

    [-n] [--normalize]
    If specified, will normalize the output image pixels to 0 and 1 values.

    [-l] [--lookuptable] <LUTcolumnToNameDirectories>
    Specifies if the label directories that are created should be named 
    according to Label Number or Label Name. 
    Can be wither "__val__", "__fs__"(uses the built in FreeSurferColorLUT.txt) 
    or <LUTFilename.txt> provided by user from the inputdir, 
    Default is "__val__" which is Label Numbers

    [-s] [--skipLabelValueList] <ListOfLabelNumbersToSkip>
    If specified as a comma separated string of label numbers,
    will not create directories of those label numbers.

    [-h] [--help]
    If specified, show help message and exit.
    
    [--json]
    If specified, show json representation of app and exit.
    
    [--man]
    If specified, print (this) man page and exit.

    [--meta]
    If specified, print plugin meta data and exit.
    
    [--savejson <DIR>] 
    If specified, save json representation file to DIR and exit. 
    
    [-v <level>] [--verbosity <level>]
    Verbosity level for app. Not used currently.
    
    [--version]
    If specified, print version number and exit. 

    [-y] [--synopsis]
    Show short synopsis.



Run
----

While ``pl-mgz2imgslices`` is meant to be run as a containerized docker image, typcially within ChRIS, it is quite possible to run the dockerized plugin directly from the command line as well. The following instructions are meant to be a psuedo- ``jupyter-notebook`` inspired style where if you follow along and copy/paste into a terminal you should be able to run all the examples.

First, let's create a directory, say ``devel`` wherever you feel like it. We will place some test data in this directory to process with this plugin.

.. code:: bash

    cd ~/
    mkdir devel
    cd devel
    export DEVEL=$(pwd)

Now, we need to fetch sample MGZ data. 

Pull MGZ data
~~~~~~~~~~~~~

- We provide a sample directory of a few ``.mgz`` volumes here. (https://github.com/FNNDSC/mgz_converter_dataset.git)

- Clone this repository (``mgz_converter_dataset``) to your local computer.

.. code:: bash

    git clone https://github.com/FNNDSC/mgz_converter_dataset.git

Make sure the ``mgz_converter_dataset`` directory is placed in the devel directory.


Using ``docker run``
~~~~~~~~~~~~~~~~~~~~

To run using ``docker``, be sure to assign an "input" directory to ``/incoming`` and an output directory to ``/outgoing``. *Make sure that the* ``$(pwd)/out`` *directory is world writable!*

- Make sure your current working directory is ``devel``. At this juncture it should contain `mgz_converter_dataset``.

- Create an output directory named ``results`` in ``devel``.

.. code:: bash

    mkdir results && chmod 777 results

- Pull the ``fnndsc/pl-mgz2imgslices`` image using the following command.

.. code:: bash

    docker pull fnndsc/pl-mgz2imgslices

Examples
--------
.. code:: bash

    mkdir in out && chmod 777 out
    docker run --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
            fnndsc/pl-mgz2imgslices mgz2imgslices.py                        \
            -i <mgzFileToConvert>                                           \
            -o <outputFileStem>                                             \
            -t <outputFileType>                                             \
            /incoming /outgoing





