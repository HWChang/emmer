#!/usr/bin/env python3


from ...main.basic.read import GetFiles, RetrospectDataImport
from ...troubleshoot.err.error import *
from ...troubleshoot.warn.warning import *

import matplotlib.pyplot as plt
import pandas
import numpy
import sys
import os

"""
Support emmer.bake Reproducibility mode

Summarizing information-rich feature calling reproducibility into basic statistics
and histogram
"""

class ReproducibilitySummary:
    """
    Summarizing information-rich feature calling statistics
    """
    def __init__(self, EMMER_reproducibility_df):
        reproducibility_in_list_of_list = EMMER_reproducibility_df.values.tolist()
        self.reproducibility = numpy.array([item for sublist in reproducibility_in_list_of_list for item in sublist])
        self.reproducibility_no_zero = self.reproducibility[self.reproducibility != 0]
        self.median = numpy.median(self.reproducibility_no_zero)
        self.mean = numpy.mean(self.reproducibility_no_zero)
        self.sd = numpy.std(self.reproducibility_no_zero)


class ReproducibilityArgs:
    """
    Take common arguments for Reproducibility modes when running bake modules

    Objective: so we can test and use @

    Argument:
        args -- Type: argparse.Namespace
                Store the user input parameters from command line
        current_wd -- Type: str
        suppress -- Type: boolean
                    Should emmer end program after error arise. Set at False when
                    running unittest
        silence -- Type: boolean

    Attributes:
        args -- Type: argparse.Namespace
        current_wd -- Type: str
        suppress -- Type: boolean
        silence -- Type: boolean
        bin_num -- Type: int
                   Number of bin used when generating histogram
        reproducibility_list -- Type: numpy.ndarray
                                One row; mulitple columns. A list of non-zero information-rich
                                feature calling reproducibility values
        input_file_num -- Type: interger
        reproducibility_summary_df -- Type: pandas.DataFrame
        warning_code -- Type: str
                        for unittest

    """
    def __init__(self, args, current_wd, suppress, silence):
        self.args = args
        self.current_wd = current_wd
        self.suppress = suppress
        self.silence = silence

        try:
            if self.args.b:
                self.bin_num = self.args.b
            else:
                raise WarningCode7(silence = self.silence)
        except WarningCode7:
            self.warning_code = '7'
            self.bin_num = 20

        try:
            if not self.args.i:
                raise Error(code = '1')
        except Error as e:
            raise ErrorCode1(suppress = self.suppress)

        if os.path.isdir(os.path.join(self.current_wd, self.args.i)) == False:
            # works on single csv file
            repro = RetrospectDataImport(file_name = os.path.join(self.current_wd, self.args.i), type = 'reproducibility')  # TODO: FileNotFoundError
            repro_summary = ReproducibilitySummary(repro.reproducibility)
            print(f'Reproducibility summary:\nmean {repro_summary.mean}\nmedian: {repro_summary.median}\nstandard deviation: {repro_summary.sd}\n')
            self.reproducibility_list = repro_summary.reproducibility_no_zero

        else:
            repro_files = GetFiles(self.args.i)
            repro_files_list = repro_files.input_files
            reproducibility_list = []

            for f in range(len(repro_files_list)):
                repro_sub = RetrospectDataImport(file_name = os.path.join(self.current_wd, repro_files_list[f]), type = 'reproducibility')
                repro_summary_sub = ReproducibilitySummary(repro_sub.reproducibility)
                reproducibility_list_sub = list(repro_summary_sub.reproducibility_no_zero)

                if f == 0:
                    reproducibility_list = reproducibility_list_sub
                    reproducibility_summary_df = repro_sub.reproducibility
                else:
                    reproducibility_list = reproducibility_list + reproducibility_list_sub
                    reproducibility_summary_df = reproducibility_summary_df.join(repro_sub.reproducibility, how = 'outer')  # similar to R merge(df.1, df.2, by = ...)

            self.input_file_num = len(repro_files_list)
            self.reproducibility_summary_df = reproducibility_summary_df.fillna(0)
            self.reproducibility_list = numpy.array(reproducibility_list)
            print(f'Reproducibility summary:\nmean {numpy.mean(self.reproducibility_list)}\nmedian: {numpy.median(self.reproducibility_list)}\nstandard deviation: {numpy.std(self.reproducibility_list)}\n')


def reproSummary(args, current_wd, retrospect_dir, output_file_tag, suppress, silence):
    #    # python3 -m emmer.bake -m 'Reproducibility' -b 20 -i emmer/data/bake_data_dir_4/information_rich_features_summary.csv

        ## take-in args
        reproducibility_args = ReproducibilityArgs(args = args, current_wd = current_wd, suppress = False, silence = False)

        if(reproducibility_args.input_file_num > 1):
            output_df_file_name = os.path.join(retrospect_dir, (output_file_tag + 'reproducibility_summary.csv'))
            reproducibility_args.reproducibility_summary_df.to_csv(output_df_file_name)

        ## make histogram
        fig = plt.figure()
        n, bins, patches = plt.hist(reproducibility_args.reproducibility_list, reproducibility_args.bin_num, range = [0, 100], facecolor='black', alpha=0.5)
        plt.xticks(numpy.arange(0, 110, 10))
        plt.xlabel('Reproducibility (%)')
        plt.ylabel('Counts')
        plt.show()
        output_file_name = os.path.join(retrospect_dir, (output_file_tag + 'reproducibility_hist.pdf'))
        fig.savefig(output_file_name, idp = 300)
