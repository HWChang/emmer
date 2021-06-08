#!/usr/bin/env python3

from ...toolbox.technical import *
from ...troubleshoot.err.error import *

import pandas
import numpy
import glob
import sys
import os


class RawDataImport:
    """
    Purpose:
        Take in a csv file name. Import data and transform to an input for NonDesityMatrix.
        Expect input has row.name (sample ID) and column name (feature name). Because without
        these information, it would be very easy for users to lose track. I hope my code would
        encourage this good practice.

    Arguments:
        file_name -- Type: str
                     file name with full path
        for_merging_file -- Type: boolean
                            Whether EMMER should raise ErrorCode when having '__' in the file name.
                            Set at 'False' when handling initial input.
        detection_limit -- Type: float
                           for self.detectionLimit()
        zero_tolerance_level -- Type: float
                                for self.zero_tolerance_level()

    Attributes:
        file_name -- Type: str
                     file name with full path
        basename -- Type: str
                    basename
        suppress -- Type: boolean
                    Whether EMMER will be terminated after rasing ErrorCode. Set at 'True' when
                    running unittest
        second_chance -- Type: boolean
                         Whether the user will have a second chance to change the input that
                         cause error or warning (This is a place holder; will add this option
                         in future update)
        raw_date -- Type: pandas.core.frame.DataFrame
        data -- Type: pandas.core.frame.DataFrame
        sample_id -- Type: list
                     row names
        feature_names -- Type: list
                         column header
        detection_limit -- Type: float
        zero_tolerance_level -- Type: float
    """

    def __init__(self, file_name, for_merging_file = False, suppress = False, second_chance = False):  ## TODO: retire second_chance

        self.file_name = file_name
        self.basename = os.path.basename(file_name)
        self.for_merging_file = for_merging_file
        self.suppress = suppress
        self.second_chance = second_chance

        # raise error when file names contain '__'
        if self.for_merging_file == False:
            try:
                if '__' in self.basename:
                    raise Error(code = '38')
            except Error as e:
                raise ErrorCode38(suppress = self.suppress) from e


    def readCSV(self):
        """
        Import data from a CSV file.
        """
        try:
            self.raw_data = pandas.read_csv(self.file_name, index_col = 0, header = 0)
        except FileNotFoundError as e:
            raise ErrorCode1(suppress = self.suppress) from e

        ## TODO: self.raw_data should only have number (no NA)
            ## TODO: or convert NA to zero


        # delete any column that only contain zeros
        self.data = self.raw_data.loc[:, (self.raw_data != 0).any(axis=0)]
        self.data = self.data.loc[(self.data != 0).any(axis=1), ]

        # update sample_id and feature_names
        self.sample_id = [str(element) for element in list(self.data.index.values)] # prevent using number as row names
        self.feature_names = [str(element) for element in list(self.data.columns.values)] # prevent using number as colnames

        if self.for_merging_file == False:
            try:
                if any('__' in element for element in self.sample_id):
                    raise Error(code = '39')
            except Error as e:
                raise ErrorCode39(suppress = self.suppress) from e

        # file_name should ended with .csv
        try:
            if not self.basename.endswith('.csv'):
                raise Error(code = '1')
        except Error as e:
            raise ErrorCode1(suppress = self.suppress) from e

        return(self.data)

    ## TODO:
    ## categorial data

    def deleteEmptyColRow(self):
        """
        Delete any column and row that only contains zeros.
        """
        self.data = self.data.loc[:, (self.data != 0).any(axis=0)]
        self.feature_names = list(self.data.columns.values)

        # delete any row that only contain zeros
        self.data = self.data.loc[(self.data != 0).any(axis=1), ]
        self.sample_id = list(self.data.index.values)
        return(self.data)

    def relativeAbundance(self):
        """
        Normalize counts for each feature by the sum of all counts in sampleself.

        Please run relativeAbundance() before setZero() and hardFilter() if you
        wish to use setZero() and hardFilter().
        """
        self.data = self.data.div(self.data.sum(axis = 1), axis = 0)

    def detectionLimit(self, detection_limit):
        self.detection_limit = detection_limit
        self.data[self.data < self.detection_limit] = 0
        self.deleteEmptyColRow()

    def hardFilter(self, zero_tolerance_level):
        """
        Manually define a hard filter to clean data based on the fraction of zero
        elements in each column.
        """
        r, c = self.data.shape
        mask = (self.data > 0).apply(numpy.count_nonzero) > numpy.round(zero_tolerance_level * r)
	    # True: the fraction of non-zero element is more then zero_tolerance_level
	    # False: otherwise
	    # test for all column and save the True/False in a vector

        self.data = self.data.loc[:, mask]
        self.data = self.deleteEmptyColRow()
        self.feature_names = list(self.data.columns.values)

	    # only keep the column if True
        return(self.data)


class RetrospectDataImport:
    """
    Import coordinate or parameter (grouping/clustering) or parameter (color/shape) setting
    file when excuting retrospect module.

    Arguments:
        file_name -- Type: str
                     file name with full path
        type -- Type: str
                Determine what the input file for

                'coordinate': Coordinates in PCA space
                'reproducibility': Information-rich calling reproducibility summary
                'vNE': Detail von Neumann entropy calculation result
                'data_color_shape_and_fill': For plotting

        dimension -- Type: str

                     'n': Not specified in input argument. Dimensionality will be determined
                          automatically
                     '2D': two dimensions
                     '3D': three dimensions

    Attributes:
        file_name -- Type: str
        coordinate -- Type: pandas.core.frame.DataFrame
        group -- Type: list
        group_set --
        individaul -- Type: list
        individual_set --
        coordinate_select_np --
        coordinate_w_info --
        reproducibility -- Type: pandas.core.frame.DataFrame
        vNE_summary --
        vNE_mean --
        vNE_sd --
        dimension --

    """

    def __init__(self, file_name, type, dimension = 'n', suppress = False):
        self.file_name = file_name

        try:
            imported_data = pandas.read_csv(self.file_name, index_col = 0, header = 0)
        except FileNotFoundError as e:
            raise ErrorCode1(suppress = suppress)

        try:
            if imported_data.isnull().values.any():
                raise Error(code = '45')
        except Error as e:
            raise ErrorCode45(suppress = suppress)

        ##--1--## coordinate
        if type == 'coordinate':
            self.coordinate = imported_data
            self.group = list([element.split("__")[0] for element in self.coordinate.index.values.tolist()])
            self.individual = list([element.split("__")[1] for element in self.coordinate.index.values.tolist()])
            self.group_set = set(self.group)
            self.individual_set = set(self.individual)

            try:
                if dimension == 'n':
                    if len(self.coordinate.columns.values) >= 3:
                        self.dimension = '3D'
                        coordinate_select = self.coordinate.iloc[:, 0:3].copy()
                    elif len(self.coordinate.columns.values) == 2:
                        self.dimension = '2D'
                        coordinate_select = self.coordinate.iloc[:, 0:2].copy()
                    else:
                        raise Error(code = '11')
                else:
                    self.dimension = dimension          # dimension in ['2D', '3D']
            except Error as e:
                raise ErrorCode11(suppress = suppress) from e

            self.coordinate_select_np = numpy.array(coordinate_select)
            self.coordinate_w_info = coordinate_select
            self.coordinate_w_info['group'] = self.group
            self.coordinate_w_info['individual'] = self.individual

        ##--2--## reproducibility
        elif type == 'reproducibility':
            repro_from_single_file = [col for col in imported_data.columns if col in ['repreducibility (%)', 'feature_name']]

            # case 1: summarized reproducibilty output
            #         row: information-rich taxa; column: group
            if len(set(repro_from_single_file)) == 0:
                self.reproducibility = imported_data
            # case 2: reproducibilty output from a single input file
            #         row: information-rich taxa; column: ['feature_name', 'occurrence', 'repreducibility (%)']
            elif len(set(repro_from_single_file)) == 2:
                self.reproducibility = pandas.DataFrame(data = numpy.array(imported_data[['repreducibility (%)']]),
                                                        columns = [os.path.basename(self.file_name)],
                                                        index = flattern(imported_data[['feature_name']].values))

        ##--3--## vNE
        elif type == 'vNE':
            self.vNE_summary = imported_data
            self.vNE_mean = numpy.mean(numpy.array(self.vNE_summary['vNE']))
            self.vNE_sd = numpy.std(numpy.array(self.vNE_summary["vNE"]), ddof = 1)

        ##--4--## data_color_shape_and_fill
        elif type == 'data_color_shape_and_fill':
            PC = [col for col in imported_data.columns if col in ['PC1', 'PC2', 'PC3']]

            try:
                if PC == ['PC1', 'PC2', 'PC3']:
                    self.dimension = '3D'
                elif PC == ['PC1', 'PC2']:
                    self.dimension = '2D'
                else:
                    raise Error(code = '29')
            except Error as e:
                raise ErrorCode29(suppress = suppress) from e


            targeted_col = [col for col in imported_data.columns if col in ['group', 'individual', 'edge_color', 'fill_color', 'shape']]
            try:
                if len(set(targeted_col)) != 5:
                    raise Error(code = '30')
            except Error as e:
                raise ErrorCode30(suppress = suppress) from e

            self.coordinate_w_info = imported_data

        ##--5--## v_df
        elif type == 'v_df':
            self.v_df = imported_data


        ##--6--## precent_explained
        elif type == 'precent_explained':
            self.precent_explained = imported_data

            try:
                if sorted(list(self.precent_explained.columns.values)) != sorted(['PC', 'percent explain', 'PC w percent explain']):
                    raise Error(code = '9')
            except Error as e:
                raise ErrorCode9(suppress = suppress) from e


class GetFiles:
    """
    Import the file names for mulitple csv files that saved under the same directory.

    Arguments:
        input_dir -- Type: str
        suppress -- Type: boolean
                    Whether exist program after error arised. Set at True when running
                    unittest
        second_chance -- Type: boolean  # TODO
                         Whether give user a second chance to re-enter the argument

    Attribute:
        input_files -- Type: list
                       A list of csv file name saved under input_dir
    """

    def __init__(self, input_dir, suppress = False, second_chance = False):
        self.input_files = glob.glob(os.path.join(input_dir, '*.csv'))

        # raise error when the folder has not csv file
        try:
            if len(self.input_files) < 1:
                raise Error(code = '1')
        except Error as e:
            raise ErrorCode1(suppress = suppress) from e


class MergeTargetedFiles:
    """
    Based on a mapping file, selected the targeted files and merged them

    Targeted file could be the individaul sequencing result. For example the first column
    could be all the ASV found in the sample, and the second column is the corresponding
    counts for each ASV. Expect target file has no row name and no header.

    Mapping file need to be a csv file that only has header, no row names and two column.
    The first column names corresponseding to the target file name. The name of the header should
    be ["file_name", "sample_id"]. The column should be the sample_id corresponding to each of the
    targeted file. This sample_id will eventually be used in RawDataImport() as the .sample_id

    The merged file will be a standard emmer.harvest args.i input file. Each row is a sample.
    Each column is a feature (e.g. ASV). Each element of the matrix is a numeric input (e.g. counts)

    Arguments:
        mapping_file -- Type: str
                        Path and name of the mapping file
        target_file_dir -- Type: str
                           Path to targeted files
        suppress -- Type: boolean
                    Whether end program after raising error. Set suppress = True
                    for unittest
        separate -- Type: str
                    Column in the targeted file separated by ?

    Attributes:
        mapping_file
        suppress
        map -- Type: pandas.DataFrame
               import from mapping file
        merged_target_file -- Type: pandas.DataFrame
                              dataframe ready for emmer.harvest analysis

    """

    def __init__(self, mapping_file, target_file_dir, separate, suppress):
        self.mapping_file = mapping_file
        self.target_file_dir = target_file_dir
        self.separate = separate
        self.suppress = suppress


    def getMap(self):
        self.map = pandas.read_csv(self.mapping_file, index_col = None, header = 0)

        try:
            if list(self.map.columns.values)[0:2] == ["file_name", "sample_id"]:
                pass
            else:
                raise Error(code = '40')
        except Error as e:
            raise ErrorCode40(suppress = self.suppress) from e


    def getTargetFile(self, targeted_file, col_name):
        df = pandas.read_csv(targeted_file, header = None, sep = self.separate)
        df = df.rename(columns = {0: 'feature', 1: col_name})
        return(df)


    def mergeFile(self):
        self.getMap()

        target_file_list = list(self.map['file_name'])
        sample_id_list = list(self.map['sample_id'])
        target_file_list_w_path = [os.path.join(self.target_file_dir, element) for element in target_file_list]

        for f in range(len(target_file_list_w_path)):
            sub = self.getTargetFile(targeted_file = target_file_list_w_path[f], col_name = sample_id_list[f])
            sub.columns.name = target_file_list[f]
            print(sub)

            if f == 0:
                merged_file = sub
            else:
                merged_file = merged_file.merge(sub, how = 'outer', on = 'feature')

        merged_file = merged_file.fillna(0)
        merged_file = merged_file.set_index('feature')
        self.merged_target_file = merged_file
