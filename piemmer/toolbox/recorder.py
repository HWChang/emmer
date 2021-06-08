#!/usr/bin/env python3

from ..troubleshoot.err.error import Error, ErrorCode44
from ..troubleshoot.inquire.input import InputCode6
import datetime
import time
import os

"""
Help to made log and record important results in  human-readable style
"""

## TODO: cover emmer.bake, error/warning/input, output dir

def initNoteBook(current_wd, script_name, script_version, tag, explicit, neglect, suppress = False):
    """
    Initate notebook for record keeping. Notebook name is stamped with time.
    To prevent initating multiple notebook for multiple emmer runs that are
    initated at the sametime, take from args.o (emmer.harvest and emmer.bake)
    to tag file name.

    When args.w == True (emmer.harvest and emmer.bake), allow user to input
    some personal massage (like the perpose of this analysis)

    Argument:
        current_wd -- Type: str
                      Current working directory
        script_name -- Type: str
                       Either 'emmer.harvest' or 'emmer.bake'
        script_version -- Type: str
                          Version of the script
        tag -- Type: str
               corresponding to agrs.o from 'emmer.harvest' or 'emmer.bake'
        explicit -- Type: boolean
                    corresponding to agrs.w from 'emmer.harvest' or 'emmer.bake'
        neglect -- Type: boolean
                   Suppress notebook initation when running unittest
        suppress -- Type: boolean
                    Suppress sys.exit() when error arised

    Reture:
        notebook_name -- Type: str
                         Notebook name with full path
    """

    if neglect == False:
        notebook_dir = os.path.join(current_wd, 'emmer_notebook')

        start_time = datetime.datetime.now()

        name_tag = ['_' + tag + '_' if tag != '' else ''][0]
        notebook_name = os.path.join(notebook_dir, 'emmer_' + str(time.mktime(start_time.timetuple()) + start_time.microsecond / 1E6) + name_tag + '_log.txt')

        ## make output dir if it does not exist
        if not os.path.exists(notebook_dir):
            os.makedirs(notebook_dir)

            try:
                if os.path.isfile(notebook_name):
                    raise Error(code = '44')
            except Error as e:
                raise ErrorCode44(suppress = suppress) from e

        notebook = open(notebook_name, "w")
        notebook.write('============================================================================================\n')
        notebook.write('Script: ' + script_name + '\n')
        notebook.write('Version: ' + script_version + '\n')
        notebook.write('Initate time: ' + str(start_time) + '\n')

        if explicit == True:
            notebook.write('\n' + InputCode6(suppress = False).input_string + '\n')

        notebook.write('============================================================================================\n')
        notebook.close()
    else:
        notebook_name = ''

    print('notebook initiate successfully...')
    return(notebook_name)


class UpdateNoteBook:
    """
    Update exitisng notebook.

    Arguments:
        notebook_name -- Type: str
                         Notebook name with full path
        neglect -- Type: boolean
                   Suppress notebook initation when running unittest

    Attributes:
        notebook_name -- Type: _io.TextIOWrapper
        neglect -- Type: boolean
    """

    def __init__(self, notebook_name, neglect):
        self.neglect = neglect
        if self.neglect == False:
            self.notebook = open(notebook_name, 'a')


    def updateArgs(self, args):
        if self.neglect == False:
            self.notebook.write('User input arguments:\n')
            args_in_str = str(args).replace('Namespace(', '    ').replace(')', '\n').replace(', ','\n    ')
            self.notebook.write(args_in_str)
            self.notebook.write('\n    Please refer to the Tutorial if you wish to know more about those arugments and their\n')
            self.notebook.write('    default settings. To view the Tutorial, run:\n')
            self.notebook.write('    python3 -m emmer.harvest -g\n')
            self.notebook.write('    python3 -m emmer.bake -g\n')
            self.notebook.write('============================================================================================\n')
            self.notebook.close()
            print('arguments import successfully...')


    def updateFilterResult(self, num_sample, num_feature, num_feature_removed, basename):
        if self.neglect == False:
            self.notebook.write(basename + '\n')
            self.notebook.write('    number of samples: ' + str(num_sample) + '\n')
            self.notebook.write('    number of features: ' + str(num_feature + num_feature_removed) + '\n')
            self.notebook.write('    number of features removed by pre-emmer data filter: ' + str(num_feature_removed) + '\n')
            self.notebook.close()


    def updateEmmerResult(self, num_info_rich):
        if self.neglect == False:
            self.notebook.write('    number of information-rich feature(s): ' + str(num_info_rich) + '\n')
            self.notebook.close()


    def updateMergeResult(self, merge_what, num_feature, norm_eigen):
        if self.neglect == False:
            self.notebook.write(merge_what + ' result\n')
            self.notebook.write('    number of feature(s): ' + str(num_feature) + '\n')
            self.notebook.write('    PC1: ' + str((norm_eigen[0])*100) + ' %\n')
            self.notebook.write('    PC2: ' + str((norm_eigen[1])*100) + ' %\n')

            if len(norm_eigen) > 2:
                self.notebook.write('    PC3: ' + str((norm_eigen[2])*100) + ' %\n')

            self.notebook.close()


    def updateProcrustesResult(self, which_dataset, procrustes_score, no_procrustes_score):
        if self.neglect == False:
            if no_procrustes_score == False:
                self.notebook.write('Procrustes test between ' + which_dataset + ' and original coordinates: ' + str(procrustes_score) + '\n')
            else:
                self.notebook.write(which_dataset + 'contains 0 feature. Skip procrustes test.')

            self.notebook.close()


    def updatePermanovaResult(self, set_seed, set_cluster, test_result):
        if self.neglect == False:
            self.notebook.write('set seed as: ' + str(set_seed) + '\n')
            self.notebook.write('grouping:\n' + str(set_cluster).replace('Name: cluster, dtype: object', '', 1) + '\n')
            self.notebook.write('\n')
            self.notebook.write(str(test_result))

        self.notebook.close()


    def updateRunTime(self, run_time):
        if self.neglect == False:
            self.notebook.write('============================================================================================\n')
            self.notebook.write('run time (exclude data merging and plotting): ' + str(run_time))
            self.notebook.close()
