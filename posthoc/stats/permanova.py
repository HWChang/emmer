#!/usr/bin/env python3


from ...main.basic.read import RetrospectDataImport
from ...troubleshoot.err.error import *
from ...troubleshoot.warn.warning import *
from ...troubleshoot.inquire.input import InputCode2
from ...toolbox.recorder import UpdateNoteBook

from skbio.stats.distance import permanova
from scipy.spatial import distance_matrix
from skbio import DistanceMatrix
import pandas
import numpy
import sys
import os


"""
Support emmer.bake Permanova mode

conduct PERMANOVA test on different groups in the PCA plot
"""

class PermanovaArgs:
    """
    Take common arguments for Permanova modes when running bake modules

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
        dist_matrix -- Type: skbio.stats.distance._base.DistanceMatrix
        group_set -- Type: set
        individual -- Type: list
        cluster -- Type: list
        coordinate_w_info -- Type: RetrospectDataImport.coordinate_w_info class object (pandas Dataframe)
                             Updated PCA coordinates with grouping information
        warning_code -- Type: str
                        for unittest

    """
    def __init__(self, args, current_wd, suppress, silence):
        # expect only args.p or args.i, not both
        if args.p:
            try:
                if args.i:
                    raise WarningCode13(silence = silence)

                parameter_df = pandas.read_csv(os.path.join(current_wd, args.p), index_col = 0, header = 0)  # TODO: FileNotFoundError  ## TODO use 'RetrospectDataImport'
                self.cluster = list(parameter_df['cluster'])

            except WarningCode13:
                self.warning_code = '13'

        else:
            try:
                if args.i:
                    print(f'Input: {args.i}\n')

                    pca_coordinate = RetrospectDataImport(file_name = os.path.join(current_wd, args.i), type = 'coordinate') # TODO: FileNotFoundError
                    self.individual = list(pca_coordinate.coordinate_w_info['individual'])
                    self.dist_matrix = DistanceMatrix(distance_matrix(pca_coordinate.coordinate_select_np, pca_coordinate.coordinate_select_np))
                    self.coordinate_w_info = pca_coordinate.coordinate_w_info
                    self.group_set = pca_coordinate.group_set
                    print(self.group_set)

                    # set parameter by interacting with users
                    cluster_map = InputCode2(set = self.group_set, suppress = suppress)
                    self.coordinate_w_info['cluster'] = self.coordinate_w_info['group'].map(cluster_map.cluster_dict)
                    self.cluster = self.coordinate_w_info['cluster']

                else:
                     raise Error(code = '8')

            except Error as e:
                raise ErrorCode8(suppress = suppress) from e


def permanovaResult(args, current_wd, retrospect_dir, output_file_tag, notebook_name, suppress, silence, neglect):
    # python3 -m emmer.bake -m 'Permanova' -i emmer/data/bake_data_dir_6/filtered_infoRich__PCA_coordinates.csv

    permanova_args = PermanovaArgs(args = args, current_wd = current_wd, suppress = suppress, silence = silence)

    ## conduct PERMANOVA
    numpy.random.seed(0)

    result = permanova(permanova_args.dist_matrix, permanova_args.cluster, permutations = 999)  ## TODO: allow user-define $permutations and $seed
    print(result)

    notebook = UpdateNoteBook(notebook_name = notebook_name, neglect =  neglect).updatePermanovaResult(set_seed = '0', set_cluster = permanova_args.cluster, test_result = result)

    parameter_df = pandas.DataFrame({'individual': permanova_args.individual, 'cluster': permanova_args.cluster})
    output_file_name = os.path.join(retrospect_dir, (output_file_tag + '_retrospect_permanova_parameter.csv'))
    parameter_df.to_csv(output_file_name)
