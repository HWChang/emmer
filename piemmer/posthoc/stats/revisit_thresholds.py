#!/usr/bin/env python3


from ...main.basic.read import RawDataImport, RetrospectDataImport, GetFiles
from ...main.advanced.iteration import InfoRichCalling, reproducibility_summary
from ...toolbox.technical import flattern, emptyNumpyArray, toFloat, floatRange
from ...troubleshoot.inquire.input import *
from ...troubleshoot.err.error import *

from ..visual.projection import ProjectionArgs, projectNew
from ..visual.viewer import RetrospectPlot, Projection
from ..visual.individual import plotIndividual

from .bifurication import identifiedFeatures
from .reproducibility import reproSummary
from .permanova import permanovaResult

from multiprocessing import Pool
from scipy.spatial import procrustes
from sklearn import linear_model
from tqdm import tqdm

import itertools
import argparse
import pandas
import numpy
import sys
import os


"""
Support emmer.bake RevisitThreshold mode
"""


def evaluateInputTuple(input_tuple, suppress = False, second_chance = False):
    """
    Make sure args.t, args.u, args.l input are logical
    """
    input_parameters = tuple(map(toFloat, input_tuple.split(',')))

    ## tuple length should be 3
    try:
        if len(input_parameters) != 3:
            raise Error(code = '17')
    except Error as e:
        if e.code == '17':
            raise ErrorCode17(suppress = suppress) from e

    ## check the first element (max) and the second element (min) values
    # input max and min need to be greater than zero
    if input_parameters != (0,0,0):
        try:
            if input_parameters[0] <= 0 or input_parameters[1] <= 0:
                raise Error(code = '20')
        except Error as e:
            raise ErrorCode20(suppress = suppress) from e

        # max need to be greater or equal to min
        try:
            if input_parameters[0] > input_parameters[1]:
                # in this case, except the third element (increment) to be...
                if input_parameters[2] <= 0:
                    raise Error(code = '24')

                # lower than max
                if input_parameters[0] <= input_parameters[2]:
                    raise Error(code = '25')

                # (input_parameters[0] - input_parameters[1]) % input_parameters[2] = 0
                if numpy.equal((input_parameters[0] - input_parameters[1]) % input_parameters[2], 0) == False:
                    raise Error(code = '22')

            elif input_parameters[0] == input_parameters[1]:
                # in this case, except the third element (increment) to be 0
                if input_parameters[2] != 0:
                    raise Error(code = '26')
            else:
                raise Error(code = '19')

        except Error as e:
            if e.code == '19':
                raise ErrorCode19(suppress = suppress) from e
            elif e.code == '22':
                raise ErrorCode22(suppress = suppress) from e
            elif e.code == '24':
                raise ErrorCode24(suppress = suppress) from e
            elif e.code == '25':
                raise ErrorCode25(suppress = suppress) from e
            elif e.code == '26':
                raise ErrorCode26(suppress = suppress) from e

    return(input_parameters)


class RevisitThresholdArgs:
    """
    Take common arguments for RevisitThreshold modes when running bake modules

    Objective: so we can test and use @

    Argument:
        args -- Type: argparse.Namespace
                Store the user input parameters from command line
        suppress -- Type: boolean
                    Should emmer end program after error arise. Set at False when
                    running unittest
        silence -- Type: boolean
        second_chance -- Type: boolean

    Attributes:
        args -- Type: argparse.Namespace
                Store the user input parameters from command line
        suppress -- Type: boolean
        silence -- Type: boolean
        second_chance -- Type: boolean
        detail_vNE --
        data_file --
        tuple_u --
        tuple_l --
        tuple_t --
        normalize -- Type: boolean
                     Scale each column in the mean centered data based on its standard deviation
                     before SVD

    """
    def __init__(self, args, current_wd, suppress, silence):
        self.args = args
        self.current_wd = current_wd
        self.suppress = suppress
        self.silence = silence


    #def getArgsN(self):
    def getArgsE(self):
        try:
#            if self.args.n:
            if self.args.e:
#                input_dir = os.path.join(self.current_wd, self.args.n)
                input_dir = os.path.join(self.current_wd, self.args.e)
                self.detail_vNE = GetFiles(input_dir = input_dir)
            else:
                raise Error(code = '13')
        except Error as e:
            raise ErrorCode13(suppress = self.suppress) from e


    def getArgsN(self):        
        if self.args.n:
            self.normalize = True
        else:
            self.normalize = False


    def getArgsI(self):
        try:
            if self.args.i:
                data_dir = os.path.join(self.current_wd, self.args.i)
                self.data_file = GetFiles(input_dir = data_dir)
            else:
                raise Error(code = '14')
        except Error as e:
            raise ErrorCode14(suppress = self.suppress) from e


    def getArgsUTL(self):
        args_u = [self.args.u if self.args.u else '0,0,0']
        args_l = [self.args.l if self.args.l else '0,0,0']
        args_t = [self.args.t if self.args.t else '0,0,0']

        three_tuples = [evaluateInputTuple(element) for element in tuple([args_u[0], args_l[0], args_t[0]])]
        self.tuple_u = three_tuples[0]
        self.tuple_l = three_tuples[1]
        self.tuple_t = three_tuples[2]

        ## should have at least one of the -u, -l, -t setting
        try:
            if sum(flattern(three_tuples)) == 0.0:
                raise Error(code = '18')
        except Error as e:
            raise ErrorCode18(suppress = self.suppress) from e


    def getArgsC(self):
        if self.args.c:
            try:
                if os.cpu_count() < self.args.c:  # TODO unittest
                    raise Error(code = '47')
                else:
                    self.num_cpu = self.args.c
            except Error as e:
                raise ErrorCode47(suppress = self.suppress) from e
        else:
            self.num_cpu = 1
        print(f'CPU: {self.num_cpu}\n')


    def getRevisitThresholdArgs(self):
        self.getArgsE()
        self.getArgsN()
        self.getArgsI()
        self.getArgsUTL()
        self.getArgsC()


class FindMinFromLM:
    """
    Purpose:
        Find the minimal distance between observation (y) and prediction (y_hat). The
        corresponding threshold setting (stored in input_df.index) represent the best
        option.

    Arguments:
        input_df -- Type: pandas.DataFrame.
                    Row represents sample. This dataframe contains five columns.
                    ['u'] u setting
                    ['l'] l setting
                    ['t'] t setting
                    ['x'] X axis: number of information-rich feature.
                    ['y'] Y axis:
                    (procurstes score between full_data and info_rich_subset) / (procurstes score between full_data and non_info_rich_subset)

    Attributes:
        input_df -- Type: pandas.DataFrame
                          x -- Type: numpy.array
                          y -- Type: numpy.array

                          Generated by FindMinFromLM class
                          y_hat -- Type: float;
                                   Explanation: fn(x)
                          y_hat_to_y -- Type: float;
                                        Explanation: fn(x) - y
        select_index -- Type: tuple;
                        Explanation: Row names of input_df. Store the threshold setting that generate the
                        corresponding x and x
        a -- Type: numpy.array;
             Explanation: regression coefficient.
        b -- Type: numpy.array; Explanation: intercept.
    """

    def __init__(self, input_df):
        self.input_df = input_df
        x = numpy.array(input_df['x']).reshape(len(input_df['x']), 1)
        y = numpy.array(input_df['y']).reshape(len(input_df['y']), 1)

        ## linear regression model
        lm = linear_model.LinearRegression()
        model = lm.fit(x, y)
        self.a = [0 if lm.coef_ < 10 ** (-8) else lm.coef_[0][0]][0]
        self.b = [0 if lm.intercept_ < 10 ** (-8) else lm.intercept_[0]][0]

        ## calculate distance along y axis between observation (y) and prediction (y_hat)
        self.input_df['y_hat'] = self.a * self.input_df['x'] - self.b
        self.input_df['y_hat_to_y'] = self.input_df['y_hat'] - self.input_df['y']
        select = self.input_df.loc[self.input_df['y_hat_to_y'] == max(self.input_df['y_hat_to_y'])]

        ## break tie
        self.select_index = select.index.values[0]  ## result may vary if use multicore


class RevisitThreshold:
    """
    Reselect information-rich features by using the detail_vNE files.
    """
    #def __init__(self, GetFiles_class_v, GetFiles_class_i, tuple_t, tuple_u, tuple_l, output_file_name, num_cpu, suppress = False):
    def __init__(self, GetFiles_class_v, GetFiles_class_i, tuple_t, tuple_u, tuple_l, output_file_name, num_cpu, normalize, suppress = False):
        self.detail_vNE_files = tuple(GetFiles_class_v.input_files)
        self.detail_vNE_basename = tuple([os.path.basename(element) for element in self.detail_vNE_files])
        self.detail_vNE_group = tuple([element.split("__")[0] for element in self.detail_vNE_basename])
        self.detail_vNE_group_set = tuple(sorted(list(set(self.detail_vNE_group))))

        self.data_files = tuple(GetFiles_class_i.input_files)
        self.data_file_basename = tuple([os.path.basename(element) for element in self.data_files])
        self.data_file_group = tuple(sorted(list([element.split("__")[0] for element in self.data_file_basename])))

        self.normalize = normalize
        self.suppress = suppress

        try:
            if list(self.detail_vNE_group_set) != sorted(list(set(self.data_file_group))):
                raise Error(code = '15')
        except Error as e:
            raise ErrorCode15(suppress = self.suppress) from e

        self.tuple_t = tuple_t
        self.tuple_u = tuple_u
        self.tuple_l = tuple_l
        self.output_file_name = output_file_name
        self.num_cpu = num_cpu


    #def singleFile(self, current_vNE_group, current_vNE_group_set_number, current_u_level, current_l_level):
    def singleFile(self, current_vNE_group, current_vNE_group_set_number, current_u_level, current_l_level):
        self.current_vNE = RetrospectDataImport(file_name = self.current_vNE_group[current_vNE_group_set_number], type = 'vNE', dimension = 'n')
        current_calling = InfoRichCalling(data = '', current_feature_names = '', upper_threshold_factor = current_u_level,
                                          lower_threshold_factor = current_l_level, direct_from_result_summary = self.current_vNE.vNE_summary,
                                          #num_cpu = 1, silence = True)  ## TODO: allow multiprocessing; add args
                                          num_cpu = 1, silence = True, normalize = self.normalize)
        current_calling.infoRichSelect()
        return(list(current_calling.info_rich_feature['feature_name']))


    def singleGroup(self, current_vNE_group_set_number, current_u_level, current_l_level, current_t_level):
        current_vNE_group = []
        target = self.detail_vNE_group_set[current_vNE_group_set_number]
        for i in range(len(self.detail_vNE_group)):
            if self.detail_vNE_group[i] == target:
                current_vNE_group.append(self.detail_vNE_files[i])
        self.current_vNE_group = current_vNE_group # pass x on to self.x for unittest; use x in computation ; TODO: update unittest code

        ## summarizing information-rich features identified in each iteration (each file) in to a dictionary
        revisit_infoRich_dict = {}
        for f in range(len(current_vNE_group)):
            current_info_rich_list = self.singleFile(current_vNE_group = current_vNE_group, current_vNE_group_set_number = f,
                                                     current_u_level = current_u_level, current_l_level = current_l_level)

            for element in current_info_rich_list:
                if element in revisit_infoRich_dict.keys():
                    revisit_infoRich_dict[element] += 1
                else:
                    revisit_infoRich_dict[element] = 1

        ## filter based on agrs.t (number of time that a feature need to be nominated as information-rich feature before it can be included
        ## in the final list of information-rich feature)
        revisit_infoRich_dict_filtered = {key:val for key, val in revisit_infoRich_dict.items() if val >= current_t_level}

        current_file = self.data_files[current_vNE_group_set_number]
        current_data_file = RawDataImport(file_name = current_file, for_merging_file = True, suppress = False, second_chance = False)
        current_data_file.readCSV()

        infoRich_reproducibility_at_specific_threshold_levels = reproducibility_summary(current_data_file.data, revisit_infoRich_dict_filtered)
        current_info_rich = list(infoRich_reproducibility_at_specific_threshold_levels['feature_name'])
        self.current_info_rich = current_info_rich  # pass x on to self.x for unittest; use x in computation; TODO: update unittest code

        singleGroup_return_dict = {'current_info_rich': current_info_rich, 'current_data_file_data': current_data_file.data, 'infoRich_reproducibility_at_specific_threshold_levels': infoRich_reproducibility_at_specific_threshold_levels}
        return(singleGroup_return_dict)


    def iteratesThroughGroupSet(self, current_u_level, current_l_level, current_t_level):
        info_rich_at_current_threshold_level_sub = []

        for g in range(len(self.detail_vNE_group_set)):
            singleGroup_return_dict = self.singleGroup(current_vNE_group_set_number = g, current_u_level = current_u_level,
                                                       current_l_level = current_l_level, current_t_level = current_t_level)
            current_info_rich = singleGroup_return_dict['current_info_rich']
            current_data_file_data = singleGroup_return_dict['current_data_file_data']
            infoRich_reproducibility_at_specific_threshold_levels = singleGroup_return_dict['infoRich_reproducibility_at_specific_threshold_levels']
            info_rich_at_current_threshold_level_sub.append(current_info_rich)

            if g == 0:
                merged_data = current_data_file_data   ##  TODO self.merged_data
                self.merged_data = current_data_file_data # pass x on to self.x for unittest; use x in computation; TODO: update unittest code
            else:
                merged_data = pandas.concat([merged_data, current_data_file_data], axis = 0, sort = True)  ##  TODO self.merged_data
                self.merged_data = merged_data # pass x on to self.x for unittest; use x in computation

        self.merged_data = self.merged_data.fillna(0) ##  TODO self.merged_data
        merged_data = merged_data.fillna(0) ##  TODO self.merged_data
        self.merged_data = merged_data # pass x on to self.x for unittest; use x in computation
        info_rich_at_current_threshold_level = list(set(flattern(info_rich_at_current_threshold_level_sub)))
        self.info_rich_at_current_threshold_level = info_rich_at_current_threshold_level # pass x on to self.x for unittest; use x in computation; TODO: update unittest code

        iteratesThroughGroupSet_return_dict = {'info_rich_at_current_threshold_level': info_rich_at_current_threshold_level, 'merged_data': merged_data}
        return(iteratesThroughGroupSet_return_dict)


    def compareBeforeAndAfterDataReduction(self, current_row):
        ## get current settings
        current_u_level = self.threshold_setting_summary['u'].iloc[current_row]
        current_l_level = self.threshold_setting_summary['l'].iloc[current_row]
        current_t_level = self.threshold_setting_summary['t'].iloc[current_row]

        ## iteration
        iteratesThroughGroupSet_return_dict = self.iteratesThroughGroupSet(current_u_level = current_u_level, current_l_level = current_l_level, current_t_level = current_t_level)
        info_rich_at_current_threshold_level = iteratesThroughGroupSet_return_dict['info_rich_at_current_threshold_level']
        merged_data = iteratesThroughGroupSet_return_dict['merged_data']

        ## when there are information-rich feature(s)
        if len(info_rich_at_current_threshold_level) > 0:
            # subset data
            non_info = [value for value in merged_data.columns.values if value not in info_rich_at_current_threshold_level]
            current_non_info = merged_data[non_info]
            self.current_non_info = current_non_info # pass x on to self.x for unittest; use x in computation; TODO: update unittest code

            current_info_rich = merged_data[info_rich_at_current_threshold_level]
            self.current_info_rich = current_info_rich # pass x on to self.x for unittest; use x in computation; TODO: update unittest code

            # project samples onto PCA space
            current_data_info_projection = Projection(merged_dataframe = merged_data, normalize = self.normalize).projection_df
            current_non_info_projection = Projection(merged_dataframe = current_non_info, normalize = self.normalize).projection_df
            current_info_rich_projection = Projection(merged_dataframe = current_info_rich, normalize = self.normalize).projection_df

            # procrustes test
            if current_info_rich_projection.shape[1] > 1:
                if current_info_rich_projection.shape[1] > 2:
                     d = 3
                else:
                     d = 2

                data_projection = numpy.array(current_data_info_projection.iloc[:, 0:d])
                non_info_projection = numpy.array(current_non_info_projection.iloc[:, 0:d])
                info_projection = numpy.array(current_info_rich_projection.iloc[:, 0:d])

                current_non_info_projection_disparity = procrustes(data_projection, non_info_projection)[2]
                current_info_projection_disparity = procrustes(data_projection, info_projection)[2]

            else:
                current_non_info_projection_disparity = numpy.nan
                current_info_projection_disparity = numpy.nan

        ## when there is no information-rich feature
        else:
            current_non_info_projection_disparity = 0
            current_info_projection_disparity = numpy.nan

        # ['current_u_level', 'current_l_level', 'current_t_level', 'num_info_rich', 'current_info_projection_disparity', 'current_non_info_projection_disparity']
        compareBeforeAndAfterDataReduction_return_list = [current_u_level, current_l_level, current_t_level, info_rich_at_current_threshold_level, current_info_projection_disparity, current_non_info_projection_disparity]
        return(compareBeforeAndAfterDataReduction_return_list)


    def iteratesThroughThresholdSetting(self):
        self.u_list = floatRange(self.tuple_u)
        self.l_list = floatRange(self.tuple_l)
        self.t_list = floatRange(self.tuple_t)

        self.iter_num = len(self.u_list) * len(self.l_list) * len(self.t_list)

        u_l = list(itertools.product(self.u_list, self.l_list))
        u_l_t_nested = list(itertools.product(self.t_list, u_l))
        threshold_setting_nested = pandas.DataFrame(u_l_t_nested, columns=['t', 'u_l'])
        threshold_setting_nested['u'] = threshold_setting_nested['u_l'].str[0]
        threshold_setting_nested['l'] = threshold_setting_nested['u_l'].str[1]
        threshold_setting = threshold_setting_nested
        threshold_setting = threshold_setting.drop(columns = ['u_l'])

        summary = pandas.DataFrame(data = emptyNumpyArray(nrow = self.iter_num, ncol = 3),
                                   columns = ['num_info_rich', 'info_to_ori_disparity', 'non_info_to_ori_disparity'])
        self.threshold_setting_summary = pandas.concat([threshold_setting, summary], axis = 1, sort = True)

        nrow = self.threshold_setting_summary.shape[0]
        threshold_setting_summary_result = [[] for i in range(nrow)]

        print('Precent threshold condition tested:')

        with Pool(processes = self.num_cpu) as p:
            with tqdm(total = nrow) as pbar:
                for i, res in enumerate(p.imap_unordered(self.compareBeforeAndAfterDataReduction, range(nrow))):
                    res[3] = len(list(set(res[3])))
                    threshold_setting_summary_result[i] = res
                    pbar.update()

        threshold_setting_result = pandas.DataFrame(data = threshold_setting_summary_result,
                                                     columns = ['u', 'l', 't', 'num_info_rich',
                                                                'info_to_ori_disparity', 'non_info_to_ori_disparity'])

        threshold_setting_result.to_csv(self.output_file_name)
        self.threshold_setting_result = threshold_setting_result
        return(threshold_setting_result)

    def compareSettings(self):
        self.threshold_setting_result['y'] = self.threshold_setting_result['info_to_ori_disparity'] / self.threshold_setting_result['non_info_to_ori_disparity']
        x_y_df = self.threshold_setting_result.loc[:,['u', 'l', 't', 'num_info_rich','y']]
        self.x_y_df = x_y_df.rename(columns = {'num_info_rich': 'x'})

        self.x_y_df = self.x_y_df.fillna(0)
        x_y_df_no_zero_in_x = self.x_y_df[self.x_y_df['x'] != 0]

        try:
            if x_y_df_no_zero_in_x.shape[0] >= 2:
                select_index = FindMinFromLM(x_y_df_no_zero_in_x)
                self.selected = x_y_df_no_zero_in_x.iloc[select_index.select_index]
            elif x_y_df_no_zero_in_x.shape[0] == 1:
                self.selected = x_y_df_no_zero_in_x
            else:
                raise Error(code = '27')
        except Error as e:
            raise ErrorCode27(suppress = self.suppress) from e


def revisitThresholdResult(args, current_wd, retrospect_dir, output_file_tag, suppress, silence):
    ## take-in args
    revisit_threshold_args = RevisitThresholdArgs(args = args, current_wd = current_wd, suppress = suppress, silence = silence)
    revisit_threshold_args.getRevisitThresholdArgs()

    print(args.o)

    output_file_name = os.path.join(retrospect_dir, (output_file_tag + '_threshold_setting_summary.csv'))

    ## revisit threshold and information-rich feature calling
    revisit_threshold = RevisitThreshold(GetFiles_class_v = revisit_threshold_args.detail_vNE, GetFiles_class_i = revisit_threshold_args.data_file,
                                         tuple_t = revisit_threshold_args.tuple_t, tuple_u = revisit_threshold_args.tuple_u,
                                         tuple_l = revisit_threshold_args.tuple_l, num_cpu = revisit_threshold_args.num_cpu,
                                         normalize = revisit_threshold_args.normalize, output_file_name = output_file_name)
    revisit_threshold.iteratesThroughThresholdSetting()
    revisit_threshold.compareSettings()
    print(f'\nSuggested threshold setting: -u {revisit_threshold.selected["u"]} -l {revisit_threshold.selected["l"]} -t {revisit_threshold.selected["t"]}')
