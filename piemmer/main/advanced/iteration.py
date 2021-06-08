#!/usr/bin/env python3

from ..basic.math import NonDesityMatrix
from ..basic.read import RawDataImport
from ...troubleshoot.warn.warning import *
from ...troubleshoot.err.error import *
from ...toolbox.recorder import UpdateNoteBook

from multiprocessing import Pool
from tqdm import tqdm

import pandas
import numpy
import time
import sys
import os

"""
This module is the basic functional unit in EMMER package. The objective of this module
is to import single dataset (a .csv file) and to select information-rich feature.


MinusOneVNE:
Systematically remove one feature from data matrix at each iteration. This class contains
functions that supports for MinDataLostFilter and InfoRichCalling

InfoRichCalling:
This class contains functions for selecting information-rich featue based on MinusOneVNE
output and selecting thresholds. Future expansion might inculde additional options for
selection criteria.

reproducibility() and reproducibility_summary():
These two functions are used to calculate and summarize the information-rich feature
call reproducibility by jackknifting data matrix (systematically remove one sample from
the data matrix at each iteration.)

Kernal:
Smallest functional unit in EMMER_vNE package. The functions in this class takes in a data
matrix (a .csv file) and filter based on user-defined parameters. Then select information-rich
features according to the user-defined threshold. Report reproducibilty upon user's request.
"""

class MinusOneVNE:
    """
    For a given RawDataImport.data matrix. Remove one feature (column) at a time and
    calculate the von Neumann entropy for the remaining matrix.

    To speed up the computation process MinusOneVNE.data is defined as a numpy.array
    """

    def __init__(self, data, normalize, feature_names, num_cpu):
        self.data = numpy.array(data)
        self.feature_names = feature_names
        self.num_cpu = num_cpu
        self.normalize = normalize

    def minusOneVNE(self, col_to_remove):
        """
        Remove specific feature from the data matrix and calculate the von Neumann entropy
        from the remaining matrix.
        """
        subset = numpy.array(self.data)
        # delete column by index
        subset = numpy.delete(subset, col_to_remove, axis = 1)

        minusOneVNE = [col_to_remove, self.feature_names[col_to_remove], NonDesityMatrix(subset, normalize = self.normalize).vNE()]
        return(minusOneVNE)

    def minusOneResult(self):
        """
        Systematically remove one feature at a time and calculate the von Neumann entropy
        for the remaining data matrix. Allow multiprocessing.
        """
        self.feature_num = len(self.feature_names)
        result_summary = [[] for i in range(self.feature_num)]

        with Pool(processes = self.num_cpu) as p:
            with tqdm(total = self.feature_num) as pbar:
                for i, res in enumerate(p.imap_unordered(self.minusOneVNE, range(self.feature_num))):
                    result_summary[i] = res
                    pbar.update()

        self.result_summary = pandas.DataFrame(data = result_summary, columns = ['feature_no', 'feature_name', 'vNE'])

        return(self.result_summary)


class InfoRichCalling:
    """
    The difference between between this and MinusOneVNE class is that this class take the
    upper and the lower boundaries for information-rich feature choosing. MinusOneVNE class
    only focus on calculating the von Neumann entropy after systematically removal of column,
    not choosing feature.

    I envision in the future I might write different ways of choosing information-rich features,
    so I create this class to store all relevent information-rich feature calling mode if the self.data
    remains unchange.
    """

    def __init__(self, data, current_feature_names, upper_threshold_factor, lower_threshold_factor,
                 num_cpu, direct_from_result_summary, normalize, silence = False, suppress = False):
        if len(direct_from_result_summary) == 0:
            self.data = numpy.array(data)
            self.feature_names = current_feature_names
            self.normalize = normalize
            self.current_result_summary = MinusOneVNE(data = self.data, normalize = self.normalize, feature_names = self.feature_names, num_cpu = num_cpu).minusOneResult()
            self.start_from_data = True
            self.force_output = False
        else:
            #self.data = data                           # not important when set direct_from_result_summary = True. Can even be ''.
            #self.feature_names = current_feature_names # not important when set direct_from_result_summary = True. Can even be ''.
            self.current_result_summary = direct_from_result_summary
            self.start_from_data = False
            self.force_output = True                    # avoid abort the program when arise ErrorCode4

        self.upper_threshold_factor = upper_threshold_factor
        self.lower_threshold_factor = lower_threshold_factor
        self.suppress = suppress
        self.silence = silence
        self.warning_code = ''


    def infoRich(self):
        """
        Select information-rich features based on the thresholds and the von Neumnann entropy.
        """

        # get threshold
        entro_mean = numpy.mean(numpy.array(self.current_result_summary["vNE"]))
        entro_sd = numpy.std(numpy.array(self.current_result_summary["vNE"]), ddof = 1)

        if self.upper_threshold_factor != 'None':
            self.upper_threshold = entro_mean + (self.upper_threshold_factor * entro_sd)
        if self.lower_threshold_factor != 'None':
            self.lower_threshold = entro_mean - (self.lower_threshold_factor * entro_sd)

        if self.upper_threshold_factor != 'None' and self.lower_threshold_factor != 'None':
            pass_condition = [(self.current_result_summary["vNE"] > self.upper_threshold) | (self.current_result_summary["vNE"] < self.lower_threshold)]
        elif self.upper_threshold_factor != 'None':
            pass_condition = [(self.current_result_summary["vNE"] > self.upper_threshold)]
        elif self.lower_threshold_factor != 'None':
            pass_condition = [(self.current_result_summary["vNE"] < self.lower_threshold)]

        tag = [1]
        self.current_result_summary["info_rich_feature"] = numpy.select(pass_condition, tag, default = 0)
        self.result_summary = self.current_result_summary

        info_rich_num = sum(numpy.array(self.current_result_summary["info_rich_feature"]))

        try:
            if info_rich_num == 0 and self.force_output == False:
                raise Error(code = 4)
        except Error as e:
            raise ErrorCode4(suppress = self.suppress) from e

        # maximum number of information-rich features
        if self.start_from_data == True:
            max_num = numpy.minimum(numpy.size(self.data, 0), numpy.size(self.data, 1))
            self.current_result_summary["max_num_for_this_dataset"] = [max_num] * self.current_result_summary.shape[0]
        else:
            max_num = self.current_result_summary["max_num_for_this_dataset"].iloc[0]

        try:
            if info_rich_num > max_num:
                raise WarningCode11(silence = self.silence)

        except WarningCode11:
            self.warning_code = '11'
            self.result_summary['deviate_from_mean'] = self.result_summary['vNE'] - entro_mean

            if self.upper_threshold_factor != 'None':
                if self.lower_threshold_factor != 'None':
                    self.result_summary['deviate_from_mean'] = abs(self.result_summary['deviate_from_mean'] - entro_mean)
                elif self.lower_threshold_factor == 'None':
                    self.result_summary['deviate_from_mean'] = self.result_summary['deviate_from_mean'] - entro_mean # TODO: need test

            elif self.upper_threshold_factor != 'None' and self.lower_threshold_factor != 'None':
                self.result_summary['deviate_from_mean'] = -(self.result_summary['deviate_from_mean'] - entro_mean)  # TODO: need test

            # rank feature-rich feature and select the ones that have higher impact on vNE when removal
            self.result_summary.sort_values(by = 'deviate_from_mean', ascending= False)
            self.reselect = list(self.result_summary[self.result_summary['info_rich_feature'] == 1].iloc[0:max_num]['feature_name'])  ##TODO: test this!!

            reselect_TF = [self.result_summary['feature_name'].isin(self.reselect)]
            self.result_summary["before_reselection"] = self.result_summary["info_rich_feature"]
            self.result_summary["info_rich_feature"] = numpy.select(reselect_TF, [1], default = 0)


    def infoRichSelect(self):
        """
        Subset infoRich result and only retain that corresponding to information-rich features
        """
        self.infoRich()
        self.info_rich_feature = self.result_summary.loc[self.result_summary["info_rich_feature"] > 0]   # <class 'pandas.core.frame.DataFrame'>


def reproducibility(InfoRichCalling_class, infoRich_dict, nrow, basename, vNE_output_folder,
                    output_file_tag, direct_from_result_summary, num_cpu, normalize):
    ## Need to be careful about the data and feature_names. They should be updated if user
    ## call the filtering function. To avoid confusion, I decided to not to list this
    ## function under MinusOneVNE or InfoRichCalling
    """
    Calculate the reproducibility of information-rich feature calling.

    This function and reproducibility_summary() are separated from InfoRichCalling_class because
    1. Aovid potential confusion regrading the data matrix (-1 row compared to the data matrix in
       InfoRichCalling_class)
    2. Easier for multiprocessing
    """
    for j in range(nrow):
        # delete row by index
        jackknift_subset = numpy.delete(InfoRichCalling_class.data, j, 0)

        info_rich_result = InfoRichCalling(data = jackknift_subset,
                                           current_feature_names = InfoRichCalling_class.feature_names,
                                           upper_threshold_factor = InfoRichCalling_class.upper_threshold_factor,
                                           lower_threshold_factor = InfoRichCalling_class.lower_threshold_factor,
                                           num_cpu = num_cpu, normalize = normalize,
                                           direct_from_result_summary = direct_from_result_summary)

        info_rich_result.infoRichSelect()

        detail_calling_result = info_rich_result.result_summary
        detail_calling_result['info_rich_feature'] = detail_calling_result['info_rich_feature'].replace([0, 1], ["No", "Yes"])
        detail_vNE_file_name = os.path.join(vNE_output_folder, basename.replace(".csv", "")) + output_file_tag + "__sub_" + str(j) + "_detail_vNE.csv"
        detail_calling_result.to_csv(detail_vNE_file_name)

        for element in info_rich_result.info_rich_feature['feature_name']:
            if element in infoRich_dict.keys():
                infoRich_dict[element] += 1
            else:
                infoRich_dict[element] = 1
    return(infoRich_dict)


def reproducibility_summary(filtered_matrix, infoRich_dict):
    filtered_matrix = numpy.array(filtered_matrix)
    nrow = numpy.size(filtered_matrix, 0)

    infoRich_dict_to_list = []

    for key, value in infoRich_dict.items():
        infoRich_dict_to_list_sub = [key, value]
        infoRich_dict_to_list.append(infoRich_dict_to_list_sub)

    infoRich_reproducibility = pandas.DataFrame(data = infoRich_dict_to_list,
                                                columns=['feature_name', 'occurrence'])
    infoRich_reproducibility['repreducibility (%)'] = infoRich_reproducibility['occurrence'] / nrow * 100
    return(infoRich_reproducibility)


class Kernal:
    """
    Smallest funcitonal unit
    """

    def __init__(self, file_name, detection_limit, tolerance, filter, upper_lim, lower_lim,
                 infoRich_threshold, quick_look, use_fractional_abundance, vNE_output_folder,
                 output_file_tag, num_cpu, notebook_name, normalize, neglect = False, silence = False,
                 suppress = False):

        self.input_matrix = RawDataImport(file_name = file_name, for_merging_file = False,
                                          suppress = False, second_chance = False)
        self.basename = os.path.basename(file_name)
        print('\nworking on: ' + self.basename)

        self.input_matrix.readCSV()
        self.detection_limit = detection_limit
        self.tolerance = tolerance
        self.filter = filter
        self.upper_lim = upper_lim
        self.lower_lim = lower_lim
        self.infoRich_threshold = infoRich_threshold
        self.quick_look = quick_look
        self.use_fractional_abundance = use_fractional_abundance
        self.vNE_output_folder = vNE_output_folder
        self.output_file_tag = output_file_tag
        self.notebook_name = notebook_name
        self.num_cpu = num_cpu
        self.neglect = neglect
        self.normalize = normalize
        self.silence = silence
        self.suppress = suppress


    def importAndProcess(self):
        if self.use_fractional_abundance == True:
            self.input_matrix.relativeAbundance()
            self.input_matrix.raw_data_before_filter = self.input_matrix.data
        else:
            self.input_matrix.raw_data_before_filter = self.input_matrix.raw_data

        if self.detection_limit > 0:
            try:
                if max(self.input_matrix.data.max()) < self.detection_limit:
                    raise Error(code = 6)
            except Error as e:
                raise ErrorCode6(suppress = self.suppress)

            self.input_matrix.detectionLimit(detection_limit = self.detection_limit)

        if self.filter:
          if self.filter == 'HardFilter':
              self.input_matrix.hardFilter(zero_tolerance_level = self.tolerance)
              self.filtered_data = self.input_matrix
          else:
              self.filtered_data = self.input_matrix

        num_sample = len(self.input_matrix.sample_id)
        num_feature = len(self.input_matrix.feature_names)
        num_feature_removed = self.input_matrix.raw_data.shape[1] - self.filtered_data.data.shape[1]

        notebook = UpdateNoteBook(notebook_name = self.notebook_name, neglect = self.neglect)
        notebook.updateFilterResult(num_sample = num_sample, num_feature = num_feature, num_feature_removed = num_feature_removed, basename = self.basename)


    def infoRichCallingAndReproducibility(self):
        self.info_rich_result = InfoRichCalling(data = self.filtered_data.data, current_feature_names = self.filtered_data.feature_names,
                                                upper_threshold_factor = self.upper_lim, lower_threshold_factor = self.lower_lim,
                                                num_cpu = self.num_cpu, normalize = self.normalize, direct_from_result_summary = '', silence = self.silence)

        if self.quick_look == True:
            print("Feature reduction with emmer...")

            self.info_rich_result.infoRichSelect()
            self.warning_code = self.info_rich_result.warning_code

            self.detail_calling_result = self.info_rich_result.result_summary
            self.detail_calling_result['info_rich_feature'] = self.detail_calling_result['info_rich_feature'].replace([0, 1], ["No", "Yes"])
            self.list_of_info_rich_features = list(self.info_rich_result.info_rich_feature['feature_name'])

            detail_vNE_file_name = os.path.join(self.vNE_output_folder, self.basename.replace(".csv", "")) + self.output_file_tag + "__detail_vNE.csv"
            self.detail_calling_result.to_csv(detail_vNE_file_name)

        else:
            print("\nCalculating the reproducibility of information-rich feature calling...")
            self.infoRich_dict = {}
            self.nrow = numpy.size(numpy.array(self.info_rich_result.data), 0)

            infoRich_dict = reproducibility(InfoRichCalling_class = self.info_rich_result, infoRich_dict = self.infoRich_dict,
                                            nrow = self.nrow, basename = self.basename, vNE_output_folder = self.vNE_output_folder,
                                            output_file_tag = self.output_file_tag, normalize = self.normalize, num_cpu = self.num_cpu,
                                            direct_from_result_summary = '')
            infoRich_dict_filtered = {key:val for key, val in infoRich_dict.items() if val >= self.infoRich_threshold}

            info_rich_features_w_reproducibility = reproducibility_summary(self.info_rich_result.data, infoRich_dict_filtered)

            r, c = info_rich_features_w_reproducibility.shape
            max_num = numpy.minimum(numpy.size(self.info_rich_result.data, 0), numpy.size(self.info_rich_result.data, 1))

            try:
                if r > max_num:
                    raise WarningCode12(silence = self.silence)
                else:
                    self.info_rich_features_w_reproducibility = info_rich_features_w_reproducibility
            except WarningCode12:
                self.warning_code = '12'
                info_rich_features_w_reproducibility = info_rich_features_w_reproducibility.sort_values(by = 'occurrence', ascending = False)
                self.info_rich_features_w_reproducibility = info_rich_features_w_reproducibility.iloc[0:max_num]

            self.list_of_info_rich_features = list(self.info_rich_features_w_reproducibility['feature_name'])

        notebook = UpdateNoteBook(notebook_name = self.notebook_name, neglect = self.neglect)
        notebook.updateEmmerResult(num_info_rich = len(self.list_of_info_rich_features))
