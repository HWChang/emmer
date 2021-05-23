#!/usr/bin/env python3


from .posthoc.stats.revisit_thresholds import revisitThresholdResult
from .posthoc.stats.bifurication import identifiedFeatures
from .posthoc.stats.reproducibility import reproSummary
from .posthoc.stats.permanova import permanovaResult

from .posthoc.visual.projection import ProjectionArgs, projectNew
from .posthoc.visual.individual import plotIndividual

from .toolbox.recorder import initNoteBook, UpdateNoteBook

from .troubleshoot.warn.warning import WarningCode9
from .troubleshoot.inquire.input import InputCode3

import argparse
import sys
import os

__version__ = '1.0'

"""
This module (emmer.bake) take in EMMER output csv files and generate plots or conduct
follow-up analyses.
"""

##==0==##
def tutorial(self):
    """
    ##==1==## Different Modes and Their Usages
    1. Individual: plot individual samples onto the PCA plot. Allow better flexibility in
                   aesthetics setting
    2. Permanova: apply PERMANOVA test on different groups in the PCA plot
    3. RevisitThreshold: revisit threshold settings (args.t, args.l, and args.u) used in
                         emmer.harvest
    4. Reproducibility: summarizing information-rich feature calling reproducibility into
                        basic statistics and histogram
    5. Bifurication: identify information-rich features that help to differentiate different
                     groups on the PCA space.
    6. Projection: project new observations onto the existing PCA space


    ##==2==##  How To
    0. General options:
       -m M, -mode        Which mode you want to use. Please refer to the Different Modes and Their Usages section above.

       optional:
       -o O               Expect a string. This string will be tag to all your output file name from the analysis.
       optional:
       -w W, -writeDownDetails
                          Do you want to add additional notes as emmer run? Default: False.
                          (Not available,. Will be included in future update)
                          Usage:
                          python3 -m emmer.harvest <other_arguments_and_inputs> -w
    ------------------------------------------------------------
    1. Individual mode:
       python3 -m emmer.bake -m 'Individual' -i emmer/data/bake_data_dir_6/filtered_infoRich__PCA_coordinates.csv

       -i I               An emmer.harvest-gereated projection file (whose file name contains the keyword 'projection' or
                          'coordinates') that stores the coordinates of each sample in PCA space.
       -a A               An emmer.harvest-gereated file that contains information about percent explained by each PC. This
                          file cound be found under 'output' with 'precent_explained' in the file name.

       optional:
       -p P               An csv file with PCA coordinates and aesthetics settings. This file will be generated after
                          you run Individual mode. You can find the file under 'revisit/''
                          You do not have to provide -i argument if you are using -p option. When providing arguments for
                          both -i and -p, emmer will ignore -i input and report warning message.

                          Should you choose to rerun this mode with, you can use
                          python3 -m emmer.bake -m 'Individual' -p where_you_store_the_file/coordinates_and_parameters.csv
    ------------------------------------------------------------
    2. Permanova mode:
       python3 -m emmer.bake -m 'Permanova' -i emmer/data/bake_data_dir_6/filtered_infoRich__PCA_coordinates.csv

       -i I               An emmer.heavest-gereated projection file (whose file name contains the keyword 'projection' or
                          'coordinates') that stores the coordinates of each sample in PCA space.
    ------------------------------------------------------------
    3. Reproducibility mode:
       python3 -m emmer.bake -m 'Reproducibility' -b 20 -i emmer/data/bake_data_dir_4/information_rich_features_summary.csv

       -b B               Number of bins used when generating the histogram under "Reproducibility" mode
       -i I               An emmer.harvest-gereated csv file that stores information-rich feature calling reproducibility
    ------------------------------------------------------------
    4. RevisitThreshold mode:
       python3 -m emmer.bake -m 'RevisitThreshold' -u 2.5,1.5,0.25 -l 2.5,1.5,0.25 -t 2,2,0 -e output/detail_vNE/ -i output/filtered_data/

       -u U               Revisit args.u (-u) setting in EMMER. Expect a three-element tuple. Example: 3,1,1 (upper bondary,
                          lower bondary, increment)
       -l L               Revisit args.l (-l) setting in EMMER. Expect a three-element tuple. Example: 3,1,1 (upper bondary,
                          lower bondary, increment)
       -t T               Revisit args.t (-t) setting in EMMER. Expect a three-element tuple. Example: 3,1,1 (upper bondary,
                          lower bondary, increment)
       -e E               A directory that store detail_vNE.csv files. The input is most likely to be 'output/detal_vNE'
       -i I               A directory that store filtered or prefilter data. The input is most likely to be 'output/filtered_data' or
                          'output/pre_filter_data'
                          Choose the folder based on whether you want to PCA plot generated from the dataset that only contains information-
                          rich features to be similar to the PCA generated from filtered_data or pre_filter_data

       optional:
       -n N, normalize    Choose this option when you set -n as True when running emmer.harvest
       -c C, -cpuNum      Support multiprocessing. This argument is used to set the number of CPU used in the analysis.
    ------------------------------------------------------------
    5. Bifurication mode:
       python3 -m emmer.bake -m 'Bifurication' -i emmer/data/bake_data_dir_4/filtered_data
                             -p emmer/data/bake_data_dir_4/information_rich_features_summary.csv
       [!] Remember to covert the above command into a single-line command if you wish to run the example

       -i I               A directory that store filtered data. The input is most likely to be 'output/filtered_data'
       -p P               An emmer-generated summary of the information-rich features.

       optional:
       -n N, normalize    Choose this option when you set -n as True when running emmer.harvest
    ------------------------------------------------------------
    6. Projection mode:
       python3 -m emmer.bake -m 'Projection' -i emmer/data/bake_data_dir_9/filtered_infoRich__PCA_coordinates.csv
                             -v emmer/data/bake_data_dir_9/filtered_infoRich__transformation_matrix.csv
                             -s emmer/data/bake_data_dir_9/filtered_infoRich__data_scaler.csv
                             -x emmer/data/bake_data_dir_9/new_observation.csv -r
       [!] Remember to covert the above command into a single-line command if you wish to run the example

       -i I                An emmer.harvest-gereated projection file (whose file name contains the keyword 'projection' or
                           'coordinates') that stores the coordinates of each sample in PCA space.
       -v V                An emmer.harvest generated csv file that stores the transformation matix. Hint: the file name that
                           contains 'transformation_matrix'.
       -s1 S1              An emmer.harvest generated csv file that stores the column means. Hint: the file name that contains '__data_colmean'
       -x X                New observations. Input directory that contains one or many csv files or a path to specific csv file.
                           Expect to have column headers and row names. Each row represents a sample and each column represents a feature.

       optional:
       -r R                Convert data into fractional abudance.
       -s2 S2              An emmer.harvest generated csv file that stores the standard deviation for each column. EMMER will generate this
                           csv file, when you set -n as True when running emmer.harvest.
                           Hint: the file name that contains '__data_colstd'
    """
    pass


class BakeCommonArgs:
    """
    Take common arguments for different modes when running bake modules

    Objective: so we can test and use @

    Argument:
        suppress -- Type: boolean
                    Should emmer end program after error arise. Set at False when
                    running unittest
        silence -- Type: boolean
                   emmer will not report warning massage when silence == True
        neglect -- Type: boolean
                   Suppress notebook initation when running unittest
        test -- Type: boolean
                Avoid running InputCode3 after trigger WarningCode9 during unittest

    Attributes:
        suppress -- Type: boolean
        args -- Type: argparse.Namespace
                Store the user input parameters from command line
        output_file_tag -- Type: str
                           Corresponding to args.o
        selected_model -- Type: str
                          Corresponding to args.m
        warning_code -- Type: str
                        For unittest
    """

    def __init__(self, suppress, silence, neglect, test):
        parser = argparse.ArgumentParser(description = '#############################################################################\nPlease use -g when you need additional explanation on different modes their corresponding arguments. Try: python3 -m emmer.harvest -g\n#############################################################################')
        parser.add_argument('-g', '-guide', action = 'store_true')
        parser.add_argument('-i', type = str)
        parser.add_argument('-a', type = str)
        parser.add_argument('-p', type = str)
        parser.add_argument('-o', type = str)
        parser.add_argument('-m', '-mode')
        parser.add_argument('-e', type = str)
        parser.add_argument('-n', '-normalize', action = 'store_true')
        parser.add_argument('-t', type = str)
        parser.add_argument('-u', type = str)
        parser.add_argument('-l', type = str)
        parser.add_argument('-b', type = int)
        parser.add_argument('-r', action = 'store_true')
        parser.add_argument('-v', type = str)
        parser.add_argument('-s1', type = str)
        parser.add_argument('-s2', type = str)
        parser.add_argument('-x', type = str)
        parser.add_argument('-c', '-cpuNum', type = int)
        parser.add_argument('-w', '-writeDownDetails', action = 'store_true')
        self.args = parser.parse_args()
        self.suppress = suppress
        self.neglect = neglect
        self.silence = silence
        self.test = test

        if self.args.g:
            print(tutorial.__doc__)
            sys.exit()


    def getArgsO(self):
        if self.args.o:
            self.output_file_tag = str(self.args.o)
        else:
            self.output_file_tag = ''


    def getArgsW(self):
        head, tail = os.path.split(os.getcwd())   # head: no last path component, which is 'revisit', in current working directory
        self.notebook_name = initNoteBook(current_wd = head, script_name = 'emmer.bake', script_version = __version__,
                                          tag = self.output_file_tag, neglect = self.neglect, explicit = self.args.w)

    def getArgsM(self):
        choice_dict = {'1': 'Individual',
                       '2': 'Permanova',
                       '3': 'RevisitThreshold',
                       '4': 'Reproducibility',
                       '5': 'Bifurication',
                       '6': 'Projection'}

        try:
            if self.args.m not in choice_dict.values() and self.args.m not in choice_dict.keys():
                raise WarningCode9(silence = self.silence)
            else:
                self.selected_model = self.args.m
        except WarningCode9:
            self.warning_code = '9'
            if self.test == False:
                model = InputCode3(set = ['mode'], choice_dict = choice_dict, suppress = False)
                self.selected_model = model.selection


    def getHomeKeepingArgs(self):
        self.getArgsO()
        self.getArgsW()
        self.getArgsM()
        UpdateNoteBook(notebook_name = self.notebook_name, neglect = self.neglect).updateArgs(args = self.args)


##==1==## set input parameters
if __name__ == '__main__':
    current_wd = os.getcwd()
    retrospect_dir = os.path.join(current_wd, 'revisit')
    if not os.path.exists(retrospect_dir):
        os.makedirs(retrospect_dir)

    os.chdir(retrospect_dir)

    common_args = BakeCommonArgs(suppress = False, silence = False, neglect = False, test = False)
    common_args.getHomeKeepingArgs()


##==2==## different bake modes
##--1--## model = 'Individual'
    # python3 -m emmer.bake -m 'Individual' -i emmer/data/bake_data_dir_6/filtered_infoRich__PCA_coordinates.csv
    if common_args.selected_model == 'Individual':
        plotIndividual(args = common_args.args, current_wd = current_wd, retrospect_dir = retrospect_dir,
                       output_file_tag = common_args.output_file_tag, suppress = False, silence = False)


##--2--## model = 'Permanova'
    # python3 -m emmer.bake -m 'Permanova' -i emmer/data/bake_data_dir_6/filtered_infoRich__PCA_coordinates.csv
    if common_args.selected_model == 'Permanova':
        permanovaResult(args = common_args.args, current_wd = current_wd, retrospect_dir = retrospect_dir,
                        output_file_tag = common_args.output_file_tag, notebook_name = common_args.notebook_name,
                        suppress = False, silence = False, neglect = False)
#        permanovaResult(args = common_args.args, current_wd = current_wd, retrospect_dir = retrospect_dir,
#                        output_file_tag = common_args.output_file_tag, suppress = False, silence = False)



##--3--## style = 'Reproducibility'
    # python3 -m emmer.bake -m 'Reproducibility' -b 20 -i emmer/data/bake_data_dir_4/information_rich_features_summary.csv
    if common_args.selected_model == 'Reproducibility':
        reproSummary(args = common_args.args, current_wd = current_wd, retrospect_dir = retrospect_dir,
                     output_file_tag = common_args.output_file_tag, suppress = False, silence = False)


##--4--## model = 'RevisitThreshold'
    # python3 -m emmer.bake -m 'RevisitThreshold' -u 2.5,1.5,0.25 -l 2.5,1.5,0.25 -e output/detail_vNE/ -i output/filtered_data/
    if common_args.selected_model == 'RevisitThreshold':
        revisitThresholdResult(args = common_args.args, current_wd = current_wd, retrospect_dir = retrospect_dir,
                               output_file_tag = common_args.output_file_tag, suppress = False, silence = False)


##--5--## model = 'Bifurication'
    # python3 -m emmer.bake -m 'Bifurication' -i emmer/data/bake_data_dir_4/filtered_data -p emmer/data/bake_data_dir_4/information_rich_features_summary.csv
    if common_args.selected_model == 'Bifurication':
        identifiedFeatures(args = common_args.args, current_wd = current_wd, retrospect_dir = retrospect_dir,
                           output_file_tag = common_args.output_file_tag, suppress = False)


##--6--## model = 'Projection'
    # python3 -m emmer.bake -m 'Projection' -i emmer/data/bake_data_dir_9/filtered_infoRich__PCA_coordinates.csv \
    #                       -v emmer/data/bake_data_dir_9/filtered_infoRich__transformation_matrix.csv \
    #                       -s emmer/data/bake_data_dir_9/filtered_infoRich__data_scaler.csv -x emmer/data/bake_data_dir_9/new_observation.csv -r
    if common_args.selected_model == 'Projection':
        new_and_old_projection_df = projectNew(args = common_args.args, current_wd = current_wd, retrospect_dir = retrospect_dir,
                                               output_file_tag = common_args.output_file_tag, suppress = False)
