pl-mgz2imageslices
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

A ChRIS DS plugin that containerizes the ``mgz2imgslices`` python module. Please use the link below for more detailed documentation on ``mgz2imgslices``:

https://github.com/FNNDSC/mgz2imgslices


Synopsis
--------

.. code::

    python mgz2imgslices.py                                             \
            [-i] [--inputFile] <inputFile>                              \
            [-o] [--outputFileStem] <outputFileStem>                    \
            [-t] [--outputFileType] <outputFileType>                    \
            [--label] <prefixForLabelDirectories>                       \
            [--saveImages]                                              \
            [-n] [--normalize]                                          \
            [-l] [--lookupTable] <LUTcolumnToNameDirectories>           \
            [--skipAllLabels]                                           \
            [-s] [--skipLabelValueList] <ListOfLabelNumbersToSkip>      \
            [-w] [--wholeVolume] <NameOfDirectoryWithAllVolumeLabels>   \
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

``pl-mgz2imageslices`` is a ChRIS-based plugin that uses ``mgz2imgslices`` to processes FreeSurfer formatted ``mgz`` volume files and create a set of output directories. Each output directory corresponds to a single voxel value in the ``mgz`` input. Within each directory are a set of ``png`` (or ``jpg``) 2D images -- each image corresponding to one slice of the original volume, and tuned/filtered to only contain that single voxel value.

For more detailed description, consult the documentation here https://github.com/FNNDSC/mgz2imgslices

**NOTE:** 

In the instances where the input ``mgz`` volume voxel values are interpreted to imply *labels* (i.e. segmented cortical regions), this plugin can use the embedded  FreeSurfer ``FreeSurferColorLUT.txt`` file to map FreeSurfer *label* IDs to human readable cortical label strings in the naming of output directories.

Arguments
---------

.. code::

    [-i|--inputFile  <inputFile>]
    Input file to convert. Should be an ``mgz`` file.

    [-o|--outputFileStem <outputFileStem>]
    The output file stem to store image conversion. If this is specified
    with an extension, this extension will be used to specify the
    output file type.

    [-t|--outputFileType <outputFileType>]
    The output file type. If different to <outputFileStem> extension,
    will override extension in favour of <outputFileType>.

    Should be a ``png`` or ``jpg``.

    [--saveImages]
    If specified as True(boolean), will save the slices of the mgz file as
    ".png" or ".jpg" image files along with the numpy files.

    [--label <prefixForLabelDirectories>]
    Prefixes the string <prefixForLabelDirectories> to each filtered
    directory name. This is mostly for possible downstream processing,
    allowing a subsequent operation to easily determine which of the output
    directories correspond to labels.

    [-n|--normalize]
    If specified, will normalize the output image pixel values to
    0 and 1, otherwise pixel image values will retain the value in
    the original input volume.

    [-l|--lookupTable <LUTfile>]
    If passed, perform a looktup on the filtered voxel label values
    according to the contents of the FreeSurferColorLUT.txt. This FreeSurferColorLUT.txt
    should conform to the FreeSurfer lookup table format (documented elsewhere).

    Note that the special <LUTfile> string ``__val__`` can be passed which
    effectively means "no <LUTfile>". In this case, the numerical voxel
    values are used for output directory names. This special string is
    really only useful for scripted cases of running this application when
    modifying the CLI is more complex than simply setting the <LUTfile> to
    ``__val__``.

    While running the docker image, you can also pass ``__fs__`` which will use
    the FreeSurferColorLUT.txt from within the docker container to perform a 
    looktup on the filtered voxel label values according to the contents of 
    the FreeSurferColorLUT.txt

    [--skipAllLabels]
    Skips all labels and converts only the whole mgz volume to png/jpg images.
    
    [-s|--skipLabelValueList <ListOfLabelNumbersToSkip>]
    If specified as a comma separated string of label numbers,
    will not create directories of those label numbers.

    [-f|--filterLabelValues <ListOfVoxelValuesToInclude>]
    The logical inverse of the [skipLabelValueList] flag. If specified,
    only filter the comma separated list of passed voxel values from the
    input volume.

    The detault value of "-1" implies all voxel values should be filtered.

    [-w|--wholeVolume <wholeVolDirName>]
    If specified, creates a diretory called <wholeVolDirName> (within the
    outputdir) containing PNG/JPG images files of the entire input.

    This effectively really creates a PNG/JPG conversion of the input
    mgz file.

    Values in the image files will be the same as the original voxel
    values in the ``mgz``, unless the [--normalize] flag is specified
    in which case this creates a single-value mask of the input image.

    [-h|--help]
    If specified, show help message and exit.

    [--json]
    If specified, show json representation of app and exit.

    [--man]
    If specified, print (this) man page and exit.

    [--meta]
    If specified, print plugin meta np_data and exit.

    [--savejson <DIR>]
    If specified, save json representation file to DIR and exit.

    [-v <level>|--verbosity <level>]
    Verbosity level for app. Not used currently.

    [--version]
    If specified, print version number and exit.

    [-y|--synopsis]
    Show short synopsis.



Run
----

While ``pl-mgz2imageslices`` is meant to be run as a containerized docker image, typcially within ChRIS, it is quite possible to run the dockerized plugin directly from the command line as well. The following instructions are meant to be a psuedo- ``jupyter-notebook`` inspired style where if you follow along and copy/paste into a terminal you should be able to run all the examples.

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

- Pull the ``fnndsc/pl-mgz2imageslices`` image using the following command.

.. code:: bash

    docker pull fnndsc/pl-mgz2imageslices

Examples
--------

Copy and modify the different commands below as needed:

.. code:: bash

    docker run --rm                                          \
        -v ${DEVEL}/mgz_converter_dataset/100307/:/incoming     \
        -v ${DEVEL}/results/:/outgoing                          \
        fnndsc/pl-mgz2imageslices mgz2imageslices.py            \
        -i aparc.a2009s+aseg.mgz                                \
        -o sample                                               \
        -t png                                                  \
        --lookupTable __val__                                   \
        --skipLabelValueList 0,2                                \
        --normalize                                             \
        --saveImages                                            \
        --wholeVolume entireVolume                              \    
        --verbosity 1                                           \
        /incoming /outgoing







