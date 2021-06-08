#!/usr/bin/env python3

from ...main.basic.read import RetrospectDataImport
from .viewer import RetrospectPlot, Projection
from ...troubleshoot.err.error import *
from ...troubleshoot.warn.warning import WarningCode13
from ...troubleshoot.inquire.input import *

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pandas
import numpy
import sys
import os

"""
Support emmer.bake Individual mode

plot individual samples onto the PCA plot. Allow better flexibility in aesthetics setting
"""


class IndividualArgs:
    """
    Take common arguments for Individual modes when running bake modules

    Argument:
        args -- Type: argparse.Namespace
                Store the user input parameters from command line
        current_wd -- Type: str
        suppress -- Type: boolean
                    Should emmer end program after error arise. Set at False when
                    running unittest
        silence -- Type: boolean

    Attributes:
        pca_coordinate -- Type: RetrospectDataImport class object (pandas Dataframe)
                          Updated PCA coordinates with plot setting (color, shape, etc.)
        warning_code -- Type: str
                        for unittest
        precent_explained -- Type: pandas Dataframe
                             Precent explained information for annotating PCs

    """

    def __init__(self, args, current_wd, suppress, silence):
        # annotate PCs
        if args.a:
            self.precent_explained = RetrospectDataImport(file_name = os.path.join(current_wd, args.a), type = 'precent_explained').precent_explained
        else:
            self.precent_explained = ''

        # have existing aesthetics parameter
        if args.p:
            try:
                if args.i:
                    raise WarningCode13(silence = silence)
                else:
                    self.warning_code = ''
            except WarningCode13:
                self.warning_code = '13'

            self.pca_coordinate = RetrospectDataImport(file_name = os.path.join(current_wd, args.p), type = 'data_color_shape_and_fill') # TODO: FileNotFoundError

        # do not have existing parameter
        else:
            try:
                if args.i and args.i.endswith('.csv'):
                    print(f'Input: {args.i}\n')
                    self.pca_coordinate = RetrospectDataImport(file_name = os.path.join(current_wd, args.i), type = 'coordinate')  # TODO: FileNotFoundError
                elif not args.i:
                    raise Error(code = '8')
                elif not args.i.endswith('.csv'):
                    raise Error(code = '8')
            except Error as e:
                if e.code == '8':
                    raise ErrorCode8(suppress = suppress) from e

            # TODO: percent explained

            #input_5_edge = InputCode5(add_msg = 'edge color of each dot', suppress = suppress, second_chance = True)
            input_5_edge = InputCode5(suppress = suppress)
            if input_5_edge.decision == ['Group'] or input_5_edge.decision == ['1']:
                print(self.pca_coordinate.group_set)
                input_1_group_edge = InputCode1(set = self.pca_coordinate.group_set, suppress = suppress)
                self.pca_coordinate.coordinate_w_info['edge_color'] = self.pca_coordinate.coordinate_w_info['group'].map(input_1_group_edge.color_dict)
            else:
                print(self.pca_coordinate.individual_set)
                input_1_individual_edge = InputCode1(set = self.pca_coordinate.individual_set, suppress = suppress)
                self.pca_coordinate.coordinate_w_info['edge_color'] = self.pca_coordinate.coordinate_w_info['individual'].map(input_1_individual_edge.color_dict)

            #input_5_fill = InputCode5(add_msg = 'fill color of each dot', suppress = suppress, second_chance = True)
            input_5_fill = InputCode5(suppress = suppress)
            if input_5_edge.decision == ['Group'] or input_5_edge.decision == ['1']:
                print(self.pca_coordinate.group_set)
                input_1_group_fill = InputCode1(set = self.pca_coordinate.group_set, suppress = suppress)
                self.pca_coordinate.coordinate_w_info['fill_color'] = self.pca_coordinate.coordinate_w_info['group'].map(input_1_group_fill.color_dict)
            else:
                print(self.pca_coordinate.individual_set)
                input_1_individual_fill = InputCode1(set = self.pca_coordinate.individual_set, suppress = suppress)
                self.pca_coordinate.coordinate_w_info['edge_color'] = self.pca_coordinate.coordinate_w_info['individual'].map(input_1_individual_fill.color_dict)

            # FIXME: cannot take shape
            #input_4_group_shape = InputCode4(set = self.pca_coordinate.group_set, add_msg = ['group'], suppress = suppress, second_chance = True)
            input_4_group_shape = InputCode4(set = self.pca_coordinate.group_set, suppress = suppress)
            self.pca_coordinate.coordinate_w_info['shape'] = self.pca_coordinate.coordinate_w_info['group'].map(input_4_group_shape.shape_dict)


def plotIndividual(args, current_wd, retrospect_dir, output_file_tag, suppress, silence):
        # python3 -m emmer.bake -m 'Individual' -i emmer/data/bake_data_dir_6/filtered_infoRich__PCA_coordinates.csv

        ## take-in args
        individual_args = IndividualArgs(args = args, current_wd = current_wd, suppress = suppress, silence = silence)

        ## generate PCA plot
        output_plot_name = os.path.join(retrospect_dir, (output_file_tag + '_individual_in_PCA.pdf'))

        if individual_args.pca_coordinate.dimension == '3D':
            plot_individauls_base_on_group = RetrospectPlot(coordinate_and_setting_df = individual_args.pca_coordinate.coordinate_w_info,
                                                            dimension = '3D', level = 'group', output_file_name = output_plot_name,
                                                            PC_annotation = individual_args.precent_explained)
        else:
            plot_individauls_base_on_group = RetrospectPlot(coordinate_and_setting_df = individual_args.pca_coordinate.coordinate_w_info,
                                                            dimension = '2D', level = 'group', output_file_name = output_plot_name,
                                                            PC_annotation = individual_args.precent_explained)

        plot_individauls_base_on_group.plot()

        output_file_name = os.path.join(retrospect_dir, (output_file_tag + '_retrospect_individaul_coloring_parameter.csv'))
        individual_args.pca_coordinate.coordinate_w_info.to_csv(output_file_name)
