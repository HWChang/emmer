#!/usr/bin/env python3

from ...main.basic.read import RawDataImport, RetrospectDataImport, GetFiles
from ...toolbox.technical import emptyNumpyArray
from ...troubleshoot.err.error import *

import pandas
import numpy
import sys
import os


"""
Support emmer.bake Projection mode

Plot new observation onto the existing PCA space. Generate a PCA with original data
points. Does not allow for customizing figure aesthetics (leave this part to emmer.bake
Individaul mode).
"""

class ProjectionArgs:
    """
    Take common arguments for Projection modes when running bake modules

    Argument:
        args -- Type: argparse.Namespace
                Store the user input parameters from command line
        current_wd -- Type: str
        suppress -- Type: boolean
                    Should emmer end program after error arise. Set at False when
                    running unittest
        #silence -- Type: boolean

    Attributes:
        original_pca_coordinate -- Type: RetrospectDataImport class object (pandas Dataframe)
                                   PCA coordinates for the original datasets.
                                   Without addition plot aesthetics setting (color, shape, etc.)
        input -- Type: list
                 A list of input file names for new observations
        v_df -- Type: Projection.V_df (pandas DataFrame) # to update
        colmean_df -- Type: RawDataImport object Projection.colmean_df (pandas DataFrame)
        normalize -- Type: boolean. Set as True when -s2 exist
        new_obs_merged -- Type: pandas DataFrame
                          new observations
    """

    def __init__(self, args, current_wd, suppress):


        ##--args.i--##
        try:
            if not args.i:
                raise Error(code = '32')
        except Error as e:
            raise ErrorCode32(suppress = suppress) from e

        try:
            if args.i.endswith('.csv') == True:
                self.original_coordinate = RawDataImport(file_name = os.path.join(current_wd, args.i), for_merging_file = True, suppress = suppress)
                self.original_coordinate.readCSV()
            else:
                raise Error(code = '32')
        except Error as e:       # could use FileNotFoundError
            raise ErrorCode32(suppress = suppress) from e


        ##--args.v--##
        try:
            if not args.v:
                raise Error(code = '34')
        except Error as e:
            raise ErrorCode34(suppress = suppress) from e


        try:
            if args.v.endswith('.csv') == True:
                self.v_df = RetrospectDataImport(file_name = os.path.join(current_wd, args.v), type = 'v_df', dimension = 'n', suppress = suppress).v_df
            else:
                raise Error(code = '34')
        except Error as e:        # could use FileNotFoundError
            raise ErrorCode34(suppress = suppress) from e


        ##--args.s1--##
        try:
            if not args.s1:
            #if not args.s:
                raise Error(code = '35')
        except Error as e:
            raise ErrorCode35(suppress = suppress) from e

        try:
            #if args.s.endswith('.csv') == True:
            #    self.scaler_df = RawDataImport(file_name = os.path.join(current_wd, args.s), for_merging_file = True, suppress = suppress)
            #    self.scaler_df.readCSV()
            if args.s1.endswith('.csv') == True:
                self.colmean_df = RawDataImport(file_name = os.path.join(current_wd, args.s1), for_merging_file = True, suppress = suppress)
                self.colmean_df.readCSV()
            else:
                raise Error(code = '35')
        except Error as e:       # could use FileNotFoundError
            raise ErrorCode35(suppress = suppress) from e


        # make sure args.v and arg.s1 have the same features names and at the same order
        try:
            if list(self.colmean_df.feature_names) != list(self.v_df.index.values):
                # self.projection_args.v_df.index.values is feature_names
                raise Error(code = '42')
        except Error as e:
            raise ErrorCode42(suppress = suppress) from e


        ##--args.s2--##
        if args.s2:
            try:
                if args.s2.endswith('.csv') == True:
                    self.colstd_df = RawDataImport(file_name = os.path.join(current_wd, args.s2), for_merging_file = True, suppress = suppress)
                    self.colstd_df.readCSV()
                else:
                    raise Error(code = '16')
            except Error as e:       # could use FileNotFoundError
                raise ErrorCode16(suppress = suppress) from e

            # make sure args.s1 and arg.s2 have the same features names and at the same order
            try:
                if list(self.colmean_df.feature_names) != list(self.colstd_df.feature_names):
                    raise Error(code = '48')
            except Error as e:
                raise ErrorCode48(suppress = suppress) from e

            self.normalize = True
        else:
            self.normalize = False


        ##--args.x--##
        try:
            if not args.x:
                raise Error(code = '43')
        except Error as e:
            raise ErrorCode43(suppress = suppress) from e

        try:
            if os.path.isdir(os.path.join(current_wd,args.x)) == True:
                self.input = GetFiles(os.path.join(current_wd, args.x)).input_files
            elif args.x.endswith('.csv') == True:
                self.input = [os.path.join(current_wd, args.x)]
            else:
                raise Error(code = '43')
        except Error as e:
            raise ErrorCode43(suppress = suppress) from e


        ## read file and merge into a single dataframe
        for f in range(len(self.input)):
            print(self.input[f])
            new_obs = RawDataImport(self.input[f], for_merging_file = False, suppress = suppress)
            new_obs.readCSV()

            index_tag = new_obs.basename.replace(".csv", "__")
            new_obs.data.index = [index_tag + element for element in new_obs.sample_id]
            new_obs.sample_id = new_obs.data.index

            if args.r:
                new_obs.relativeAbundance()

            if len(self.input) == 0 or f == 0:
                self.new_obs_merged = new_obs.data
            else:
                self.new_obs_merged = pandas.concat([self.new_obs_merged, new_obs.data], axis = 0, sort = True)


        ## make sure the order of column are the same as colmean_df
        new_obs_merged_ordered = pandas.DataFrame(data = emptyNumpyArray(nrow = self.new_obs_merged.shape[0], ncol = len(self.colmean_df.feature_names)),
                                                  columns = self.colmean_df.feature_names, index = self.new_obs_merged.index.values)

        for c in range(len(list(self.colmean_df.feature_names))):
            in_merged_data = self.colmean_df.feature_names[c] in self.new_obs_merged.columns.values
            if in_merged_data == True:
                new_obs_merged_ordered[[self.colmean_df.feature_names[c]]] = self.new_obs_merged[[self.colmean_df.feature_names[c]]]
            else:
                new_obs_merged_ordered[[self.colmean_df.feature_names[c]]] = 0
                ## TODO: need unittest; raise WarningCode?

        self.new_obs_merged_ordered = new_obs_merged_ordered.fillna(0)


def projectNew(args, current_wd, retrospect_dir, output_file_tag, suppress):
    """
    write something...
    """
    projection_args = ProjectionArgs(args = args, current_wd = current_wd, suppress = suppress)

    ## minus colmean_df and matmul with V
    nrow = projection_args.new_obs_merged_ordered.shape[0]
    new_observation_df = projection_args.new_obs_merged_ordered
    colmean = numpy.array(projection_args.colmean_df.data)
    V = numpy.array(projection_args.v_df)

    ncol_V = numpy.size(V, 1)
    PC_list = list(['PC' + str(i) for i in range(1 , (ncol_V + 1))])
    mean_centered_matrix = numpy.array(new_observation_df) - numpy.tile(colmean, (nrow, 1))

    if projection_args.normalize == True:
        colstd = numpy.array(projection_args.colstd_df.data.iloc[0, ])
        scaled_mean_centered_matrix = numpy.matmul(mean_centered_matrix, numpy.diag(1/colstd))   ### FIXME  ##PC order?
        projection = numpy.matmul(scaled_mean_centered_matrix, V)
    else:
        projection = numpy.matmul(mean_centered_matrix, V)

    projection_df = pandas.DataFrame(projection, columns = PC_list, index = new_observation_df.index.values)
    #print(projection_df.columns.values)


    ## TODO: PC1, PC10, PC11, PC2 ... need reorder
    output_file_name = os.path.join(retrospect_dir, (output_file_tag + '__retrospect_project_new.csv'))
    projection_df.to_csv(output_file_name)

    ## merge the coordinates from new and original dataset
    original_and_new_coordinates_df = pandas.concat([projection_args.original_coordinate.data, projection_df], axis = 0, sort = True)
    original_and_new_coordinates_df = original_and_new_coordinates_df.fillna(0)

    output_file_name = os.path.join(retrospect_dir, (output_file_tag + '__retrospect_both_new_and_original_coordinates.csv'))
    original_and_new_coordinates_df.to_csv(output_file_name)

    return(original_and_new_coordinates_df)
