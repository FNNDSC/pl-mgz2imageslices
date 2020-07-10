#!/usr/bin/env python                                            
#
# mgz2imgslices ds ChRIS plugin app
#
# (c) 2016-2019 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#


import os
import sys
import numpy as np
import nibabel as nib
import imageio
import pandas as pd
import re
sys.path.append(os.path.dirname(__file__))
import  pfmisc
from    pfmisc._colors      import  Colors
from    pfmisc.debug        import  debug


# import the Chris app superclass
from chrisapp.base import ChrisApp


Gstr_title = """
                      _____ _                     _ _               
                     / __  (_)                   | (_)              
 _ __ ___   __ _ ____`' / /'_ _ __ ___   __ _ ___| |_  ___ ___  ___ 
| '_ ` _ \ / _` |_  /  / / | | '_ ` _ \ / _` / __| | |/ __/ _ \/ __|
| | | | | | (_| |/ / ./ /__| | | | | | | (_| \__ \ | | (_|  __/\__ \\
|_| |_| |_|\__, /___|\_____/_|_| |_| |_|\__, |___/_|_|\___\___||___/
            __/ |                        __/ |                      
           |___/                        |___/                       
"""

Gstr_synopsis = """

(Edit this in-line help for app specifics. At a minimum, the 
flags below are supported -- in the case of DS apps, both
positional arguments <inputDir> and <outputDir>; for FS apps
only <outputDir> -- and similarly for <in> <out> directories
where necessary.)

    NAME

       mgz2imgslices.py 

    SYNOPSIS

        python mgz2imgslices.py                                         \\
            [-i] [--inputFile] <inputFile>                              \\
            [-o] [--outputFileStem] <outputFileStem>                    \\
            [-t] [--outputFileType] <outputFileType>                    \\
            [-n] [--normalize]                                          \\
            [-h] [--help]                                               \\
            [--json]                                                    \\
            [--man]                                                     \\
            [--meta]                                                    \\
            [--savejson <DIR>]                                          \\
            [-v <level>] [--verbosity <level>]                          \\
            [--version]                                                 \\
            [-y] [--synopsis]                                           \\
            <inputDir>                                                  \\
            <outputDir> 

    BRIEF EXAMPLE

        * Bare bones execution

            mkdir in out && chmod 777 out
            python mgz2imgslices.py   \\
                                in    out

    DESCRIPTION

        `mgz2imgslices.py` ...

    ARGS

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

        [-h] [--help]
        If specified, show help message and exit.
        
        [--json]
        If specified, show json representation of app and exit.
        
        [--man]
        If specified, print (this) man page and exit.

        [--meta]
        If specified, print plugin meta nparr_data and exit.
        
        [--savejson <DIR>] 
        If specified, save json representation file to DIR and exit. 
        
        [-v <level>] [--verbosity <level>]
        Verbosity level for app. Not used currently.
        
        [--version]
        If specified, print version number and exit. 

        [-y] [--synopsis]
        Show short synopsis.

"""


class Mgz2imgslices(ChrisApp):
    """
    An app to ....
    """
    AUTHORS                 = 'FNNDSC (dev@babyMRI.org)'
    SELFPATH                = os.path.dirname(os.path.abspath(__file__))
    SELFEXEC                = os.path.basename(__file__)
    EXECSHELL               = 'python3'
    TITLE                   = 'A ChRIS plugin app that converts mgz files to png or jpeg alongwith some special features that make it usable even as part of other project workflows.'
    CATEGORY                = ''
    TYPE                    = 'ds'
    DESCRIPTION             = 'An app to convert mgz volumes to png or jpeg (more easilt viewable) formats'
    DOCUMENTATION           = 'https://github.com/FNNDSC/pl-mgz2imgslices'
    VERSION                 = '0.1'
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

        self.add_argument('-i', '--inputFile', dest='inputFile', type=str,
                          optional=False, help='name of the input file within the inputDir')

        self.add_argument('-o', '--outputFileStem', dest='outputFileStem', type=str, optional=True,
                          help='output file', default='sample')

        self.add_argument('-t', '--outputFileType', dest='outputFileType', type=str,
                          default='png', optional=True, help='output image file format')

        self.add_argument('-n', '--normalize', dest='normalize', type=bool, 
                            default=False, optional=True, help='normalize the pixels of output image files')

        self.add_argument('-l', '--lookuptable', dest='lookuptable', type=str, 
                            default='__val__', optional=True, help='reads name for the Label directories')

        self.add_argument('-y', '--synopsis', dest='synopsis', type=bool, action='store_true',
                          default=False, optional=True, help='short synopsis')

        self.add_argument('-s', '--skipLabelValueList', dest='skipLabelValueList', type=str, 
                          default='', optional=True, help='Comma separated list of labels to skip')

        # add an arg for creating an output img of the *whole* mgz vol... maybe "--wholeVolume" (bool)


    def initialize(self, options):

        self.l_skip             = []
        self.__name__           = "mgz2imgslices"
        self.verbosity          = int(options.verbosity)
        self.dp                 = pfmisc.debug(    
                                            verbosity   = self.verbosity,
                                            within      = self.__name__
                                            )

    def readFSColorLUT(self, str_filename):
        l_column_names = ["#No", "LabelName"]

        df_FSColorLUT = pd.DataFrame(columns=l_column_names)

        with open(str_filename) as f:
            for line in f:
                if line and line[0].isdigit():
                    line = re.sub(' +', ' ', line)
                    l_line = line.split(' ')
                    l_labels = l_line[:2]
                    df_FSColorLUT.loc[len(df_FSColorLUT)] = l_labels
            
        return df_FSColorLUT

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        print(Gstr_title)
        print('Version: %s' % self.get_version())

        self.initialize(options)

        if len(options.skipLabelValueList):
            self.l_skip         = options.skipLabelValueList.split(',')

        mgz_vol = nib.load("%s/%s" % (options.inputdir, options.inputFile))

        nparr_mgz_vol = mgz_vol.get_fdata()
        
        unique, counts = np.unique(nparr_mgz_vol, return_counts=True)
        labels = dict(zip(unique, counts))

        for item in labels:
            if int(item) in self.l_skip: 
                print(item)
                continue
            self.dp.qprint("Processing %s.." % item, level = 1)
            if options.lookuptable == "__val__":
                str_dirname = str(int(item))
            elif options.lookuptable == "__fs__":
                df_FSColorLUT = self.readFSColorLUT("/usr/src/mgz2imgslices/FreeSurferColorLUT.txt")
                str_dirname = df_FSColorLUT.loc[df_FSColorLUT['#No'] == str(int(item)), 'LabelName'].iloc[0]
            else:
                df_FSColorLUT = self.readFSColorLUT("%s/%s" % (options.inputdir, options.lookuptable))
                str_dirname = df_FSColorLUT.loc[df_FSColorLUT['#No'] == str(int(item)), 'LabelName'].iloc[0]
                
            os.mkdir("%s/%s" % (options.outputdir, str_dirname))

            #mask voxels other than the current label to 0 values
            if(options.normalize):
                nparr_single_label = np.where(nparr_mgz_vol!=item, 0, 1)
            else:
                nparr_single_label = np.where(nparr_mgz_vol!=item, 0, item)
            
            i_total_slices = nparr_single_label.shape[0]
            # iterate through slices
            for current_slice in range(0, i_total_slices):
                nparr_data = nparr_single_label[:, :, current_slice]
                
                # prevents lossy conversion
                nparr_data=nparr_data.astype(np.uint8)

                str_image_name = "%s/%s/%s-%00d.%s" % (options.outputdir, str_dirname, 
                    options.outputFileStem, current_slice, options.outputFileType)
                self.dp.qprint("Saving %s" % str_image_name, level = 2)
                imageio.imwrite(str_image_name, nparr_data)

    def show_man_page(self):
        """
        Print the app's man page.
        """
        print(Gstr_synopsis)


# ENTRYPOINT
if __name__ == "__main__":
    chris_app = Mgz2imgslices()
    chris_app.launch()
