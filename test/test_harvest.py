#!/usr/bin/env python3

## usage
# at a level above emmer/
# python3 -m emmer.test.test_harvest

from ..main.basic.math import NonDesityMatrix
from ..main.basic.read import RawDataImport, GetFiles
from ..main.advanced.iteration import MinusOneVNE, InfoRichCalling, reproducibility, reproducibility_summary, Kernal
#from ..main.advanced.iteration import MinusOneVNE, MinDataLostFilter, InfoRichCalling, reproducibility, reproducibility_summary, Kernal
from ..harvest import HarvestArgs, EMMER, mergeDataFrame
from ..troubleshoot.err.error import *

from pandas.util.testing import assert_frame_equal

import unittest
import argparse
import shutil
import pandas
import numpy
import glob
import sys
import os


class TestHarvestArgs(unittest.TestCase):

    def test_getArgsI(self):
        print('\ntest_TestHarvestArgs.getArgsI:')
        print('        case 1: non csv file when input a specific file')
        sys.argv[1:] = ['-i', 'emmer/data/sow_test_dir_2/targert_file_1.txt']
        with self.assertRaises(ErrorCode1):
            processed_args = HarvestArgs(suppress = True, silence = False, neglect = True)
            processed_args.getArgsI()
        print('===========================================================')


    def test_getArgsQT(self):
        print('\ntest_TestHarvestArgs.getArgsQT:')
        print('        case 1: do not need to set args.t when use args.q')
        sys.argv[1:] = ['-t', '2', '-q']
        processed_args = HarvestArgs(suppress = True, silence = False, neglect = True)
        processed_args.getArgsQT()
        my_result = processed_args.warning_code
        expected_result = '10'
        self.assertEqual(my_result, expected_result)
        print('===========================================================')


    def test_getArgsFZ(self):
        print('\ntest_TestHarvestArgs.getArgsFZ:')
        print('        case 1: test error handling')
        print('             1.1: unexpected agrs.z number setting when using HardFilter')
        sys.argv[1:] = ['-f', 'HardFilter', '-z', '2']
        with self.assertRaises(ErrorCode2):
            processed_args = HarvestArgs(suppress = True, silence = False, neglect = True)
            processed_args.getArgsFZ()

        print('        ---------------------------------------------------')
        print('             1.2: missing agrs.z when using HardFilter')
        sys.argv[1:] = ['-f', 'HardFilter']
        with self.assertRaises(ErrorCode3):
            processed_args = HarvestArgs(suppress = True, silence = False, neglect = True)
            processed_args.getArgsFZ()

        print('        ---------------------------------------------------')
        print('             1.3: set agrs.z when using None filter')
        sys.argv[1:] = ['-f', 'None', '-z', '0.5']
        processed_args = HarvestArgs(suppress = True, silence = False, neglect = True)
        processed_args.getArgsFZ()
        my_result = processed_args.warning_code
        expected_result = '2'
        self.assertEqual(my_result, expected_result)
        print('===========================================================')


    def test_getArgsUL(self):
        print('\ntest_TestHarvestArgs.getArgsUL:')
        print('        case 1: missing both args.u and args.l settings')
        sys.argv[1:] = ['-f', 'None', '-z', '0.5']
        with self.assertRaises(ErrorCode5):
            processed_args = HarvestArgs(suppress = True, silence = False, neglect = True)
            processed_args.getArgsUL()
        print('===========================================================')


    def test_getArgsPS(self):
        print('\ntest_TestHarvestArgs.getArgsPS:')
        print('        case 1: args.s warning handling')
        print('             1.1: current version of emmer can not generate args.s plots when working on specific csv (args.i)')
        sys.argv[1:] = ['-i', 'emmer/data/data_dir_3/group_A.csv', '-s']
        #with self.assertRaises(WarningCode3):
        processed_args = HarvestArgs(suppress = True, silence = False, neglect = True)
        processed_args.getArgsI()
        processed_args.getArgsPS()
        my_result = processed_args.warning_code
        expected_result = '3'
        self.assertEqual(my_result, expected_result)

        print('        ---------------------------------------------------')
        print('             1.2: current version of emmer can not generate args.s plots when input directory only contains one csv file')
        sys.argv[1:] = ['-i', 'emmer/data/data_dir_1/', '-s']
        #with self.assertRaises(WarningCode3):
        processed_args = HarvestArgs(suppress = True, silence = False, neglect = True)
        processed_args.getArgsI()
        processed_args.getArgsPS()
        my_result = processed_args.warning_code
        expected_result = '3'
        self.assertEqual(my_result, expected_result)

        print('        ---------------------------------------------------')
        print('        case 2: args.p warning handling')
        print('             2.1: current version of emmer can not generate args.p plots when working on specific csv (args.i)')
        sys.argv[1:] = ['-i', 'emmer/data/data_dir_3/group_A.csv', '-p']
        #with self.assertRaises(WarningCode5):
        processed_args = HarvestArgs(suppress = True, silence = False, neglect = True)
        processed_args.getArgsI()
        processed_args.getArgsPS()
        my_result = processed_args.warning_code
        expected_result = '5'
        self.assertEqual(my_result, expected_result)

        print('        ---------------------------------------------------')
        print('             2.2: current version of emmer can not generate args.p plots when input directory only contains one csv file')
        sys.argv[1:] = ['-i', 'emmer/data/data_dir_1', '-p']
        #with self.assertRaises(WarningCode6):
        processed_args = HarvestArgs(suppress = True, silence = False, neglect = True)
        processed_args.getArgsI()
        processed_args.getArgsPS()
        my_result = processed_args.warning_code
        expected_result = '5'
        self.assertEqual(my_result, expected_result)
        print('===========================================================')


    def test_getArgsC(self):
        print('\ntest_TestHarvestArgs.getArgsC:')
        print('        case 1: args.c warning handling')
        print('             1.1: user set args.c at 0')
        sys.argv[1:] = ['-c', '0']
        with self.assertRaises(ErrorCode47):
            processed_args = HarvestArgs(suppress = True, silence = False, neglect = True)
            processed_args.getArgsC()

        print('        ---------------------------------------------------')
        print('             1.2: args.c > CPU in the computer')
        sys.argv[1:] = ['-c', '10000000000']
        with self.assertRaises(ErrorCode47):
            processed_args = HarvestArgs(suppress = True, silence = False, neglect = True)
            processed_args.getArgsC()

        print('        ---------------------------------------------------')
        print('        case 2: default setting')
        sys.argv[1:] = []
        processed_args = HarvestArgs(suppress = True, silence = False, neglect = True)
        processed_args.getArgsC()
        my_result = processed_args.num_cpu
        expected_result = 1
        self.assertEqual(my_result, expected_result)
        print('===========================================================')


class TestEMMER(unittest.TestCase):

    def test_EMMER(self):
        print('\ntest_EMMER:')
        print('    input_dir: "emmer/data/data_dir_1"')
        input_dir = 'emmer/data/data_dir_1'
        print('    output_file_tag: "test1"')
        output_file_tag = 'test1'
        print('    detection_limit: 0')
        detection_limit = 0
        print('    tolerance: 1')
        tolerance = 1
        print('    filter: "None"')
        filter = 'None'
        print('    upper_threshold_factor: 1')
        upper_threshold_factor = 1
        print('    lower_threshold_factor: 1')
        lower_threshold_factor = 1
        print('    specific_csv: False')
        specific_csv = False
        print('    information-rich threshold: 1')
        infoRich_threshold = 1
        print('    quick_look: True')
        quick_look = True
        print('    use_fractional_abundance: True')
        use_fractional_abundance = True
        print('    normalize: False')
        normalize = False
        print('    num_cpu: 1')
        num_cpu = 1

        one_file = EMMER(input_dir = input_dir, output_file_tag = output_file_tag,
                         detection_limit = detection_limit, tolerance = tolerance,
                         filter = filter, upper_threshold_factor = upper_threshold_factor,
                         lower_threshold_factor = lower_threshold_factor,
                         specific_csv = specific_csv, infoRich_threshold = infoRich_threshold,
                         notebook_name = '', neglect = '', normalize = normalize,
                         num_cpu = num_cpu, quick_look = quick_look,
                         use_fractional_abundance = use_fractional_abundance)
        my_result = one_file.input_file_names

        expected_result = ['emmer/data/data_dir_1/test_case_1.csv']
        self.assertListEqual(my_result, expected_result)
        shutil.rmtree('output')
        print('===========================================================')


    def test_singleFile(self):
        print('        ---------------------------------------------------')
        print('        case 1: HardFilter')
        print('             1.1: hypothetical data')
        print('    input_dir: "emmer/data/data_dir_1"')
        input_dir = 'emmer/data/data_dir_1'
        print('    output_file_tag: "test1"')
        output_file_tag = 'test1'
        print('    detection_limit: 0')
        detection_limit = 0
        print('    tolerance: 0.6')
        tolerance = 0.6
        print('    filter: "HardFilter"')
        filter = 'HardFilter'
        print('    upper_threshold_factor: 1')
        upper_threshold_factor = 1
        print('    lower_threshold_factor: 1')
        lower_threshold_factor = 1
        print('    specific_csv: True')
        specific_csv = False
        print('    information-rich threshold: 1')
        infoRich_threshold = 1
        print('    quick_look: True')
        quick_look = True
        print('    use_fractional_abundance: True')
        use_fractional_abundance = True
        print('    normalize: False')
        normalize = False
        print('    num_cpu: 1')
        num_cpu = 1

        one_file = EMMER(input_dir = input_dir, output_file_tag = output_file_tag,
                         detection_limit = detection_limit, tolerance = tolerance,
                         filter = filter, upper_threshold_factor = upper_threshold_factor,
                         lower_threshold_factor = lower_threshold_factor,
                         specific_csv = specific_csv, infoRich_threshold = infoRich_threshold,
                         notebook_name = '', neglect = '', normalize = normalize,
                         num_cpu = num_cpu, quick_look = quick_look,
                         use_fractional_abundance = use_fractional_abundance)

        one_file.singleFile()

        my_result = list(one_file.data.filtered_data.data.columns.values)

        expected_result = ['col1', 'col2', 'col3', 'col5', 'col6']
        self.assertListEqual(my_result, expected_result)

        ## filter: HardFilter; real data
        print('        ---------------------------------------------------')
        print('             1.2: read data (check each filtering steps)')
        print('             1.2.1: raw data')
        print('    input_dir: "emmer/data/data_dir_3/group_A.csv"')
        input_dir = 'emmer/data/data_dir_3/group_A.csv'
        print('    output_file_tag: "test1"')
        output_file_tag = 'test1'
        print('    detection_limit: 0.001')
        detection_limit = 0.001
        print('    tolerance: 0.33')
        tolerance = 0.33
        print('    filter: "HardFilter"')
        filter = 'HardFilter'
        print('    upper_threshold_factor: 1')
        upper_threshold_factor = 1
        print('    lower_threshold_factor: 1')
        lower_threshold_factor = 1
        print('    specific_csv: True')
        specific_csv = True
        print('    information-rich threshold: 1')
        infoRich_threshold = 1
        print('    quick_look: True')
        quick_look = True
        print('    use_fractional_abundance: True')
        use_fractional_abundance = True
        print('    normalize: False')
        normalize = False
        print('    num_cpu: 1')
        num_cpu = 1

        one_file = EMMER(input_dir = input_dir, output_file_tag = output_file_tag,
                         detection_limit = detection_limit, tolerance = tolerance,
                         filter = filter, upper_threshold_factor = upper_threshold_factor,
                         lower_threshold_factor = lower_threshold_factor,
                         specific_csv = specific_csv, infoRich_threshold = infoRich_threshold,
                         notebook_name = '', neglect = '', normalize = normalize,
                         num_cpu = num_cpu, quick_look = quick_look,
                         use_fractional_abundance = use_fractional_abundance)

        one_file.singleFile()


        # Raw data; after removing empty rows and columns
        my_result = list(one_file.data.input_matrix.raw_data.shape)
        expected_result = [13, 4809]
        self.assertListEqual(my_result, expected_result)


        # After removing empty rows and columns
        print('        ---------------------------------------------------')
        print('             1.2.2: after removing empty rows and columns')
        my_result = list(one_file.data.input_matrix.raw_data_before_filter.shape)
        expected_result = [13, 1077]
        self.assertListEqual(my_result, expected_result)


        # After data filtering
        print('        ---------------------------------------------------')
        print('             1.2.3: after filtering')
        my_result = list(one_file.data.input_matrix.data.shape)
        expected_result = [13, 126]
        self.assertListEqual(my_result, expected_result)


        ## filter: None
        print('        ---------------------------------------------------')
        print('        case 2: No filter')
        print('    input_dir: "emmer/data/data_dir_1"')
        input_dir = 'emmer/data/data_dir_1'
        print('    output_file_tag: "test1"')
        output_file_tag = 'test1'
        print('    detection_limit: 0')
        detection_limit = 0
        print('    tolerance: 1')
        tolerance = 1
        print('    filter: "None"')
        filter = 'None'
        print('    upper_threshold_factor: 1')
        upper_threshold_factor = 1
        print('    lower_threshold_factor: 1')
        lower_threshold_factor = 1
        print('    specific_csv: False')
        specific_csv = False
        print('    information-rich threshold: 1')
        infoRich_threshold = 1
        print('    quick_look: True')
        quick_look = True
        print('    use_fractional_abundance: True')
        use_fractional_abundance = True
        print('    normalize: False')
        normalize = False
        print('    num_cpu: 1')
        num_cpu = 1

        one_file = EMMER(input_dir = input_dir, output_file_tag = output_file_tag,
                         detection_limit = detection_limit, tolerance = tolerance,
                         filter = filter, upper_threshold_factor = upper_threshold_factor,
                         lower_threshold_factor = lower_threshold_factor,
                         specific_csv = specific_csv, infoRich_threshold = infoRich_threshold,
                         notebook_name = '', neglect = '', normalize = normalize,
                         num_cpu = num_cpu, quick_look = quick_look,
                         use_fractional_abundance = use_fractional_abundance)

        one_file.singleFile()
        my_result = list(one_file.data.filtered_data.data.columns.values)

        expected_result = ['col1', 'col2', 'col3', 'col4', 'col5', 'col6']
        self.assertListEqual(my_result, expected_result)
        shutil.rmtree('output')
        print('===========================================================')


    def test_multipleFiles(self):
        print('        ---------------------------------------------------')
        print('        case 1: set quick_look at False')
        print('    input_dir: "emmer/data/data_dir_2"')
        input_dir = 'emmer/data/data_dir_2'
        print('    output_file_tag: "multipleFiles_test1"')
        output_file_tag = 'multipleFiles_test2'
        print('    detection_limit: 0')
        detection_limit = 0
        print('    tolerance: 1')
        tolerance = 1
        print('    filter: "None"')
        filter = 'None'
        print('    upper_threshold_factor: 1')
        upper_threshold_factor = 1
        print('    lower_threshold_factor: 1')
        lower_threshold_factor = 1
        print('    specific_csv: False')
        specific_csv = False
        print('    information-rich threshold: 2')
        infoRich_threshold = 2
        print('    quick_look: False')
        quick_look = False
        print('    use_fractional_abundance: True')
        use_fractional_abundance = True
        print('    normalize: False')
        normalize = False
        print('    num_cpu: 1')
        num_cpu = 1

        one_file = EMMER(input_dir = input_dir, output_file_tag = output_file_tag,
                         detection_limit = detection_limit, tolerance = tolerance,
                         filter = filter, upper_threshold_factor = upper_threshold_factor,
                         lower_threshold_factor = lower_threshold_factor,
                         specific_csv = specific_csv, infoRich_threshold = infoRich_threshold,
                         notebook_name = '', neglect = '', normalize = normalize,
                         num_cpu = num_cpu, quick_look = quick_look,
                         use_fractional_abundance = use_fractional_abundance)

        one_file.multipleFiles()

        my_result = one_file.summary_df

        data = [[0.00, 28.57],
                [50.00, 0.00],
                [66.67, 0.00],
                [0.00, 100.00],
                [33.33, 0.00],
                [66.67, 0.00]]
        expected_result = pandas.DataFrame(data, columns = ['test_case_1.csv', 'test_case_2.csv'],
                                           index = ['col1', 'col2', 'col3', 'col4', 'col5', 'col6'])

        assert_frame_equal(my_result, expected_result)

        print('        ---------------------------------------------------')
        print('        case 2: set quick_look at True')
        print('    input_dir: "emmer/data/data_dir_2"')
        input_dir = 'emmer/data/data_dir_2'
        print('    output_file_tag: "multipleFiles_test1"')
        output_file_tag = 'multipleFiles_test2'
        print('    detection_limit: 0')
        detection_limit = 0
        print('    tolerance: 1')
        tolerance = 1
        print('    filter: "None"')
        filter = 'None'
        print('    upper_threshold_factor: 1')
        upper_threshold_factor = 1
        print('    lower_threshold_factor: 1')
        lower_threshold_factor = 1
        print('    specific_csv: False')
        specific_csv = False
        print('    information-rich threshold: 1')
        infoRich_threshold = 1
        print('    quick_look: True')
        quick_look = True
        print('    use_fractional_abundance: True')
        use_fractional_abundance = True
        print('    normalize: False')
        normalize = False
        print('    num_cpu: 1')
        num_cpu = 1

        one_file = EMMER(input_dir = input_dir, output_file_tag = output_file_tag,
                         detection_limit = detection_limit, tolerance = tolerance,
                         filter = filter, upper_threshold_factor = upper_threshold_factor,
                         lower_threshold_factor = lower_threshold_factor,
                         specific_csv = specific_csv, infoRich_threshold = infoRich_threshold,
                         notebook_name = '', neglect = '', normalize = normalize,
                         num_cpu = num_cpu, quick_look = quick_look,
                         use_fractional_abundance = use_fractional_abundance)

        one_file.multipleFiles()

        my_result = one_file.summary_df

        data = [[1.0, 0.0],
                [1.0, 0.0],
                [0.0, 1.0],
                [1.0, 0.0]]
        expected_result = pandas.DataFrame(data, columns = ['test_case_1.csv', 'test_case_2.csv'],
                                           index = ['col2', 'col3', 'col4', 'col6'])

        assert_frame_equal(my_result, expected_result)
        shutil.rmtree('output')
        print('===========================================================')


class TestMergeDataFrame(unittest.TestCase):
    def test_mergeDataFrame(self):
        print('\ntest_mergeDataFrame:')
        print('    input_dir: "emmer/data/data_dir_2"')
        input_dir = 'emmer/data/data_dir_2'
        print('    output_file_tag: "test2"')
        output_file_tag = 'test2'
        print('    detection_limit: 0')
        detection_limit = 0
        print('    tolerance: 1')
        tolerance = 1
        print('    filter: "None"')
        filter = 'None'
        print('    upper_threshold_factor: 1')
        upper_threshold_factor = 1
        print('    lower_threshold_factor: 1')
        lower_threshold_factor = 1
        print('    specific_csv: False')
        specific_csv = False
        print('    information-rich threshold: 1')
        infoRich_threshold = 1
        print('    quick_look: True')
        quick_look = True
        print('    use_fractional_abundance: True')
        use_fractional_abundance = True
        print('    normalize: False')
        normalize = False
        print('    num_cpu: 1')
        num_cpu = 1

        one_file = EMMER(input_dir = input_dir, output_file_tag = output_file_tag,
                         detection_limit = detection_limit, tolerance = tolerance,
                         filter = filter, upper_threshold_factor = upper_threshold_factor,
                         lower_threshold_factor = lower_threshold_factor,
                         specific_csv = specific_csv, infoRich_threshold = infoRich_threshold,
                         notebook_name = '', neglect = '', normalize = normalize,
                         num_cpu = num_cpu, quick_look = quick_look,
                         use_fractional_abundance = use_fractional_abundance)

        one_file.multipleFiles()
        transform_info = mergeDataFrame(EMMER_class = one_file, select = 'filtered_infoRich',
                                        file_name_list = one_file.clean_df_file_names,
                                        info_rich_list = one_file.collections_of_info_rich_features,
                                        notebook_name = '', normalize = normalize, neglect = True)

        my_result = one_file.merged_dataframe.shape
        expected_result = (13, 4)

        self.assertEqual(my_result, expected_result)
        shutil.rmtree('output')
        print('===========================================================')


if __name__ == '__main__':
    unittest.main()
