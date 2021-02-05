#
# DS plugin wrapper about an underlying `mgz2imgslices`
#
# (c) 2016-2021 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

# Turn off all logging for modules in this libary.
import logging
logging.disable(logging.CRITICAL)

import os
import sys
import traceback
from pydoc import synopsis

import numpy as np
import nibabel as nib
import imageio
import pandas as pd
import re
sys.path.append(os.path.dirname(__file__))
import  pfmisc
from    pfmisc._colors      import  Colors
from    pfmisc.debug        import  debug

import time
# import the Chris app superclass
from chrisapp.base import ChrisApp
from mgz2imgslices import mgz2imgslices


Gstr_title = """
       _                             _____ _                                 _ _               
      | |                           / __  (_)                               | (_)              
 _ __ | |______ _ __ ___   __ _ ____`' / /'_ _ __ ___   __ _  __ _  ___  ___| |_  ___ ___  ___ 
| '_ \| |______| '_ ` _ \ / _` |_  /  / / | | '_ ` _ \ / _` |/ _` |/ _ \/ __| | |/ __/ _ \/ __|
| |_) | |      | | | | | | (_| |/ / ./ /__| | | | | | | (_| | (_| |  __/\__ \ | | (_|  __/\__ \ 
| .__/|_|      |_| |_| |_|\__, /___|\_____/_|_| |_| |_|\__,_|\__, |\___||___/_|_|\___\___||___/
| |                        __/ |                              __/ |                            
|_|                       |___/                              |___/                             
"""


class Mgz2imgslices(ChrisApp):
    """
    A ChRIS plugin app that converts mgz files to png or jpeg (with optional label color lookup).
    """
    AUTHORS                 = 'FNNDSC (dev@babyMRI.org)'
    SELFPATH                = os.path.dirname(os.path.abspath(__file__))
    SELFEXEC                = os.path.basename(__file__)
    EXECSHELL               = 'python3'
    TITLE                   = 'A ChRIS plugin app that converts mgz files to png or jpeg (with optional label color lookup).'
    CATEGORY                = ''
    TYPE                    = 'ds'
    DESCRIPTION             = 'An app to convert mgz volumes to numpy arrays and png image formats'
    DOCUMENTATION           = 'https://github.com/FNNDSC/pl-mgz2imgslices'
    VERSION                 = '2.0.4'
    ICON                    = '' # url of an icon image
    LICENSE                 = 'Opensource (MIT)'
    MAX_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MIN_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MAX_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MIN_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MAX_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_GPU_LIMIT           = 0  # Override with the minimum number of GPUs, as an integer, for your plugin
    MAX_GPU_LIMIT           = 0  # Override with the maximum number of GPUs, as an integer, for your plugin

    # Use this dictionary structure to provide key-value output descriptive information
    # that may be useful for the next downstream plugin. For example:
    #
    # {
    #   "finalOutputFile":  "final/file.out",
    #   "viewer":           "genericTextViewer",
    # }
    #
    # The above dictionary is saved when plugin is called with a ``--saveoutputmeta``
    # flag. Note also that all file paths are relative to the system specified
    # output directory.
    OUTPUT_META_DICT = {}

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        Use self.add_argument to specify a new app argument.
        """

        self.add_argument(  '-i', '--inputFile',
                            dest        = 'inputFile',
                            type        = str,
                            optional    = False,
                            help        ='name of the input file within the inputDir')

        self.add_argument(  '-o', '--outputFileStem',
                            dest        = 'outputFileStem',
                            type        = str,
                            optional    = True,
                            help        = 'output file',
                            default     = 'sample')

        self.add_argument(  '-t', '--outputFileType',
                            dest        = 'outputFileType',
                            type        = str,
                            default     = 'png',
                            optional    = True,
                            help        = 'output image file format')

        self.add_argument(  '--saveImages',
                            dest        = 'saveImages',
                            type        = bool,
                            action      = 'store_true',
                            default     = False,
                            optional    = True,
                            help        = 'store png images for each slice of mgz file')

        self.add_argument(  '--label',
                            dest        = 'label',
                            type        = str,
                            default     = 'label',
                            optional    = True,
                            help        = 'prefix a label to all the label directories')

        self.add_argument(  '-n', '--normalize',
                            dest        = 'normalize',
                            type        = bool,
                            action      = 'store_true',
                            default     = False,
                            optional    = True,
                            help        = 'normalize the pixels of output image files')

        self.add_argument(  '-l', '--lookupTable',
                            dest        = 'lookupTable',
                            type        = str,
                            default     = '__none__',
                            optional    = True,
                            help        = 'reads name for the Label directories')

        self.add_argument(  '-y', '--synopsis',
                            dest        = 'synopsis',
                            type        = bool,
                            action      = 'store_true',
                            default     = False,
                            optional    = True,
                            help        = 'short synopsis')

        self.add_argument(  '--skipAllLabels',
                            dest        = 'skipAllLabels',
                            type        = bool,
                            action      = 'store_true',
                            default     = False,
                            optional    = True,
                            help        = 'skip all labels and create only whole Volume images')

        self.add_argument(  '-s', '--skipLabelValueList',
                            dest        = 'skipLabelValueList',
                            type        = str,
                            default     = '',
                            optional    = True,
                            help        = 'Comma separated list of labels to skip')

        self.add_argument(  '-f', '--filterLabelValueList',
                            dest        = 'filterLabelValueList',
                            type        = str,
                            default     = '-1',
                            optional    = True,
                            help        = 'Comma separated list of voxel values to include')

        self.add_argument(  '-w', '--wholeVolume',
                            dest        = 'wholeVolume',
                            type        = str,
                            default     = "wholeVolume",
                            optional    = True,
                            help        = 'Converts entire mgz volume to png/jpg instead of individually masked labels')

        self.add_argument(  '--printElapsedTime',
                            dest        = 'printElapsedTime',
                            type        = bool,
                            action      = 'store_true',
                            default     = False,
                            optional    = True,
                            help        = 'print program run time')

        self.add_argument("--verbose",
                            type        = str,
                            optional    = True,
                            help        = "verbosity level for app",
                            dest        = 'verbose',
                            default     = "1")


    def show_man_page(self, ab_shortOnly=False):
        scriptName = os.path.basename(sys.argv[0])
        shortSynopsis = '''
        NAME

    	    pl-mgz2imgslices - convert mgz volumes to jpg/png/etc.

        SYNOPSIS
            -i|--inputFile <inputFile>                                  \\
            -d|--outputDir <outputDir>                                  \\
            [-I|--inputDir <inputDir>]                                  \\
            [-o|--outputFileStem]<outputFileStem>]                      \\
            [-t|--outputFileType <outputFileType>]                      \\
            [--saveImages]                                              \\
            [--label <prefixForLabelDirectories>]                       \\
            [-n|--normalize]                                            \\
            [-l|--lookupTable <LUTfile>]                                \\
            [--skipAllLabels]                                           \\
            [-s|--skipLabelValueList <ListOfVoxelValuesToSkip>]         \\
            [-f|--filterLabelValueList <ListOfVoxelValuesToInclude>]    \\
            [-w|--wholeVolume <wholeVolDirName>]                        \\
            [-h|--help]                                                 \\
            [--json]                                                    \\
            [--man]                                                     \\
            [--meta]                                                    \\
            [--savejson <DIR>]                                          \\
            [-v|--verbosity <level>]                                    \\
            [--version]                                                 \\
            [-y|--synopsis]


        ''' % scriptName

        description = '''
        DESCRIPTION

        ``mgz2imgslices`` is a simple Python utility that filters "labels"
        from ``mgz`` volume files and saves each label set as slices of
        (by default) ``png`` files, organized into a series of directories,
        one per label set.

        An ``mgz`` format file simply contains a 3D volume data structure of
        image values. Often these values are interpreted to be image
        intensities. Sometimes, however, they can be interpreted as label
        identifiers. Regardless of the interpretation, the volume image data
        is simply a number value in each voxel of the volume.

        This script will scan across the input ``mgz`` volume, and for each
        voxel value create a new output directory. In that directory will be
        a set of (typically) ``png`` images, one per slice of the original
        volume. These images will only contain the voxels in the original
        dataset that all had that particular voxel value.

        In this manner, ``mgz2imgslices`` can also be thought of as a dynamic
        filter of an ``mgz`` volume file that filters each voxel value into
        its own output directory of ``png`` image files.

        ARGS

            [-i|--inputFile  <inputFile>]
            Input file to convert. Should be an ``mgz`` file.

            [-o|--outputFileStem <outputFileStem>]
            The output file stem to store image conversion. If this is specified
            with an extension, this extension will be used to specify the
            output file type.

            [-t|--outputFileType <outputFileType>]
            The output file type. If different to <outputFileStem> extension,
            will override extension in favour of <outputFileType>.

            Should be a ``png``.

            [--saveImages]
            If specified as True(boolean), will save the slices of the mgz file as
            ".png" image files along with the numpy files.

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
            If passed, perform a lookup on the filtered voxel label values
            according to the contents of the <LUTfile>. This <LUTfile> should
            conform to the FreeSurfer lookup table format (documented elsewhere).

            Note that the special <LUTfile> string ``__val__`` can be passed which
            effectively means "no <LUTfile>". In this case, the numerical voxel
            values are used for output directory names. This special string is
            really only useful for scripted cases of running this application when
            modifying the CLI is more complex than simply setting the <LUTfile> to
            ``__val__``.

            [--skipAllLabels]
            Skips all labels and converts only the whole mgz volume to png/jpg images.

            [-s|--skipLabelValueList <ListOfLabelNumbersToSkip>]
            If specified as a comma separated string of label numbers,
            will not create directories of those label numbers.

            [-f|--filterLabelValueList <ListOfVoxelValuesToInclude>]
            The logical inverse of the [skipLabelValueList] flag. If specified,
            only filter the comma separated list of passed voxel values from the
            input volume.

            The default value of "-1" implies all voxel values should be filtered.

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

        GITHUB

            o See https://github.com/FNNDSC/mgz2imgslices for more help and source.

                ''' % (scriptName)

        if ab_shortOnly:
            return shortSynopsis
        else:
            return shortSynopsis + description

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        print(Gstr_title)
        print('Version: %s' % self.get_version())

        try:
            options.inputDir = options.inputdir
            options.outputDir = options.outputdir
            options.verbosity = options.verbose

            imgConverter = mgz2imgslices.object_factoryCreate(options).C_convert

            if options.version:
                print("Version: %s" % options.version)
                sys.exit(1)

            if options.man or options.synopsis:
                if options.man:
                    str_help = self.show_man_page(False)
                else:
                    str_help = self.show_man_page(True)
                print(str_help)
                sys.exit(1)

            imgConverter.tic()
            imgConverter.run()

            # if b_dicomExt:
            #     break

            if options.printElapsedTime:
                print("Elapsed time = %f seconds" % imgConverter.toc())
                sys.exit(0)

        except Exception as e:
            traceback.print_exc()



# ENTRYPOINT
if __name__ == "__main__":
    app = Mgz2imgslices()
    app.launch()
