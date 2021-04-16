## usage
# at a level above emmer/
# python3 -m emmer.test.test_revisit_threshold

from ..main.basic.read import RawDataImport, RetrospectDataImport, GetFiles
from ..main.advanced.iteration import MinusOneVNE, InfoRichCalling, reproducibility_summary
from ..bake import BakeCommonArgs
from ..posthoc.stats.revisit_thresholds import RevisitThresholdArgs, FindMinFromLM, evaluateInputTuple, floatRange, RevisitThreshold
from ..troubleshoot.err.error import *
#from ..troubleshoot.warn.warning import *

from itertools import compress
import numpy.testing
import argparse
import unittest
import pandas
import numpy
import time
import sys
import os



class TestRevisitThresholdArgs(unittest.TestCase):

    def test_getArgsV(self):
        print('\ntest_RevisitThreshold.getArgsN:')
        print('        case 1: missing args.n setting')
        sys.argv[1:] = ['-m', 'RevisitThreshold']
        processed_args = BakeCommonArgs(suppress = True, test = False, neglect = True, silence = False)
        processed_args.getHomeKeepingArgs()

        with self.assertRaises(ErrorCode13):
            revisit_threshold_args = RevisitThresholdArgs(args = processed_args.args, current_wd = '', suppress = True, silence = False)
            revisit_threshold_args.getArgsE()
        print('===========================================================')


    def test_getArgsI(self):
        print('\ntest_RevisitThreshold.getArgsI:')
        print('        case 1: missing args.i setting')
        sys.argv[1:] = ['-m', 'RevisitThreshold']
        processed_args = BakeCommonArgs(suppress = True, test = False, neglect = True, silence = False)
        processed_args.getHomeKeepingArgs()

        with self.assertRaises(ErrorCode14):
            revisit_threshold_args = RevisitThresholdArgs(args = processed_args.args, current_wd = '', suppress = True, silence = False)
            revisit_threshold_args.getArgsI()
        print('===========================================================')


    def test_getArgsUTL(self):
        print('\ntest_RevisitThreshold.getArgsUTL:')
        print('        case 1: have no args.l, args.u, and args.t setting')
        sys.argv[1:] = ['-m', 'RevisitThreshold']
        processed_args = BakeCommonArgs(suppress = True, test = False, neglect = True, silence = False)
        processed_args.getHomeKeepingArgs()

        with self.assertRaises(ErrorCode18):
            revisit_threshold_args = RevisitThresholdArgs(args = processed_args.args, current_wd = '', suppress = True, silence = False)
            revisit_threshold_args.getArgsUTL()
        print('===========================================================')


    def test_getRevisitThresholdArgs(self):   # TODO
        pass


class TestEvaluateInputTuple(unittest.TestCase):

    def test_passing(self):
        print('\ntest_EvaluateInputTuple.passing:')
        print('        case 1: passing test condition')
        print('             1.1: an reasonalbe input that != 0,0,0')
        print('        -t: "2,1,1"')
        args_t = '2,1,0.5'

        my_result = evaluateInputTuple(args_t)
        expected_result = (2,1,0.5)
        self.assertEqual(my_result, expected_result)

        print('        ---------------------------------------------------')
        print('             1.2: an input that == 0,0,0')
        print('        -t: "0,0,0"')
        args_t = '0,0,0'

        my_result = evaluateInputTuple(args_t)
        expected_result = (0,0,0)
        self.assertEqual(my_result, expected_result)
        print('===========================================================')


    def test_error17(self):
        print('\ntest_EvaluateInputTuple.error17:')
        print('        -t: "2,2,2,1"')
        args_t = '2,2,2,1'

        with self.assertRaises(ErrorCode17):
            output = evaluateInputTuple(args_t, suppress = True, second_chance = False)
        print('===========================================================')


    def test_error20(self):
        print('\ntest_EvaluateInputTuple.error20:')
        print('        Case 1: first element less than 0')
        print('        -t: "-2,2,1"')
        args_t = '-2,2,1'

        with self.assertRaises(ErrorCode20):
            output = evaluateInputTuple(args_t, suppress = True, second_chance = False)


        ## Case 1: confirm the function generate a empty array
        print('        ---------------------------------------------------')
        print('        Case 2: second element equals to 0')
        print('        -t: "2,0,1"')
        args_t = '2,0,1'

        with self.assertRaises(ErrorCode20):
            output = evaluateInputTuple(args_t, suppress = True, second_chance = False)
        print('===========================================================')


    def test_error19(self):
        print('\ntest_EvaluateInputTuple.error19:')
        print('        -t: "1,2,1"')
        args_t = '1,2,1'

        with self.assertRaises(ErrorCode19):
            output = evaluateInputTuple(args_t, suppress = True, second_chance = False)
        print('===========================================================')


    def test_error24(self):
        print('\ntest_EvaluateInputTuple.error24:')
        print('        -t: "3,2,0"')
        args_t = '3,2,0'

        with self.assertRaises(ErrorCode24):
            output = evaluateInputTuple(args_t, suppress = True, second_chance = False)
        print('===========================================================')


    def test_error22(self):
        print('\ntest_EvaluateInputTuple.error22:')
        print('        -t: "3,2,2"')
        args_t = '3,2,2'

        with self.assertRaises(ErrorCode22):
            output = evaluateInputTuple(args_t, suppress = True, second_chance = False)
        print('===========================================================')


    def test_error25(self):
        print('\ntest_EvaluateInputTuple.error25:')
        print('        -t: "3,2,7"')
        args_t = '3,2,7'

        with self.assertRaises(ErrorCode25):
            output = evaluateInputTuple(args_t, suppress = True, second_chance = False)
        print('===========================================================')


    def test_error26(self):
        print('\ntest_EvaluateInputTuple.error26:')
        print('        -t: "2,2,7"')
        args_t = '2,2,7'

        with self.assertRaises(ErrorCode26):
            output = evaluateInputTuple(args_t, suppress = True, second_chance = False)
        print('===========================================================')


class TestFloatRange(unittest.TestCase):

    def test_floatRange(self):
        print('\ntest_floatRange:')
        print('        input_tuple = (3, 1, 0.5)')
        input_tuple = (3, 1, 0.5)

        my_result = floatRange(input_tuple)
        expected_result = [1, 1.5, 2, 2.5, 3]
        self.assertEqual(my_result, expected_result)
        print('===========================================================')


class TestFindMinFromLM(unittest.TestCase):

    def test_FindMinFromLM(self):
        print('\ntest_FindMinFromLM:')
        data = {'x':[1, 2, 3, 4, 5, 6], 'y':[2.2, 4.2, 6.2, 8.2, 10.2, 12.2]}
        input_df = pandas.DataFrame(data, index =['sample1', 'sample2', 'sample3', 'sample4', 'sample5', 'sample6'])

        on_original_axises = FindMinFromLM(input_df)

        print('        Case 1: linear regression')
        print('             1.1: regression correlation')
        my_result = on_original_axises.a
        expected_result = 2
        numpy.testing.assert_almost_equal(my_result, expected_result)

        print('        ---------------------------------------------------')
        print('             1.2: intercept')
        my_result = on_original_axises.b
        expected_result = 0.2
        numpy.testing.assert_almost_equal(my_result, expected_result)

        print('')
        print('        Case 2: find entry that has the minimal distance from regression line')
        print('        ---------------------------------------------------')
        print('             2.1: only one minimal value')
        data = {'x':[1, 2, 3, 4, 5, 6], 'y':[2, 3.9, 6.5, 8, 10.7, 11.5]}
        input_df = pandas.DataFrame(data, index =['sample1', 'sample2', 'sample3', 'sample4', 'sample5', 'sample6'])
        on_original_axises = FindMinFromLM(input_df)

        my_result = list([on_original_axises.select_index])
        expected_result = ['sample6']
        self.assertEqual(my_result, expected_result)


        print('        ---------------------------------------------------')
        print('             2.2: denominator')
        data = {'x':[1, 2, 3, 4, 5, 6, 6], 'y':[2, 3.9, 6.5, 8, 10.7, 11.5, 11.5]}
        input_df = pandas.DataFrame(data, index =['sample1', 'sample2', 'sample3', 'sample4', 'sample5', 'sample6', 'sample7'])
        on_original_axises = FindMinFromLM(input_df)

        my_result = list([on_original_axises.select_index])
        expected_result = ['sample6']
        self.assertEqual(my_result, expected_result)
        print('===========================================================')


class TestRevisitThreshold(unittest.TestCase):

    def test_getFileV(self):
        print('\ntest_RevisitThreshold.getFileV:')
        print('        -v: "emmer/data/retrospect_data_dir_2/detail_vNE/"]')
        args_v = 'emmer/data/retrospect_data_dir_2/detail_vNE/'
        detail_vNE = GetFiles(input_dir = args_v)
        detail_vNE_basename = list([os.path.basename(element) for element in detail_vNE.input_files])
        detail_vNE_group = list([element.split("__")[0] for element in detail_vNE_basename])

        my_result = len(detail_vNE_group)
        expected_result = 30

        self.assertEqual(my_result, expected_result)
        print('===========================================================')


    def test_getFileI(self):
        print('\ntest_RevisitThreshold.getFileI:')
        print('        -i: "emmer/data/retrospect_data_dir_2/pre_filter_data/"')
        args_i = 'emmer/data/retrospect_data_dir_2/pre_filter_data/'
        data_dir = os.path.join(os.getcwd(), args_i)
        data_file = GetFiles(input_dir = data_dir)
        data_file_basename = list([os.path.basename(element) for element in data_file.input_files])
        data_file_group = list([element.split("__")[0] for element in data_file_basename])

        my_result = len(data_file_group)
        expected_result = 2

        self.assertEqual(my_result, expected_result)
        print('===========================================================')


    def test_error15(self):
        print('\ntest_RevisitThreshold.init:')
        print('        case 1: check input -v and -i')
        print('        -v: "emmer/data/retrospect_data_dir_2/detail_vNE/"]')
        args_v = 'emmer/data/retrospect_data_dir_2/detail_vNE/'
        input_dir = os.path.join(os.getcwd(), args_v)
        detail_vNE = GetFiles(input_dir = args_v)
        print('        -i: "emmer/data/retrospect_data_dir_2/pre_filter_data_not_match/"')
        args_i = 'emmer/data/retrospect_data_dir_2/pre_filter_data_cause_error_15/'
        data_dir = os.path.join(os.getcwd(), args_i)
        data_file = GetFiles(input_dir = data_dir)
        print('        -t: "2,1,1"')
        args_t = '2,1,1'
        tuple_t = evaluateInputTuple(args_t)
        print('        -u: "2,1,1"')
        args_u = '2,1,1'
        tuple_u = evaluateInputTuple(args_u)
        print('        -l: "2,1,1')
        args_l = '2,1,1'
        tuple_l = evaluateInputTuple(args_l)
        print('        output_file_name: "test.csv"')
        output_file_name = 'test.csv'
        print('        current_vNE_group_set_number: 1')
        current_vNE_group_set_number = 1
        print('    normalize: False')
        normalize = False

        if os.cpu_count() > 1:
            num_cpu = os.cpu_count() - 1
            print(f'    num_cpu: {num_cpu}')
        else:
            print('    num_cpu: 1')
            num_cpu = 1
            print('    your computer only have one CPU; unable to test multiprocessing function')

        with self.assertRaises(ErrorCode15):
            revisit_threshold = RevisitThreshold(GetFiles_class_v = detail_vNE, GetFiles_class_i = data_file,
                                                 tuple_t = tuple_t, tuple_u = tuple_u, tuple_l = tuple_l,
                                                 output_file_name = output_file_name, num_cpu = num_cpu,
                                                 normalize = normalize, suppress = True)


    def test_singleFile(self):
        print('\ntest_RevisitThreshold.singleFile:')

        ## case 1: check the number of file for a specific group
        #       1.1: group B
        print('        case 1: check the number of file for a specific group')
        print('             1.1: group B')
        print('        -v: "emmer/data/retrospect_data_dir_2/detail_vNE/"]')
        args_v = 'emmer/data/retrospect_data_dir_2/detail_vNE/'
        input_dir = os.path.join(os.getcwd(), args_v)
        detail_vNE = GetFiles(input_dir = args_v)
        print('        -i: "emmer/data/retrospect_data_dir_2/pre_filter_data/"')
        args_i = 'emmer/data/retrospect_data_dir_2/pre_filter_data/'
        data_dir = os.path.join(os.getcwd(), args_i)
        data_file = GetFiles(input_dir = data_dir)
        print('        -t: "3,1,1"')
        args_t = '3,1,1'
        tuple_t = evaluateInputTuple(args_t)
        print('        -u: "3,1,1"')
        args_u = '3,1,1'
        tuple_u = evaluateInputTuple(args_u)
        print('        -l: "2,1,1')
        args_l = '2,1,1'
        tuple_l = evaluateInputTuple(args_l)
        print('        output_file_name: "test216.csv"')
        output_file_name = 'test216.csv'
        print('        current_vNE_group_set_number: 1')
        current_vNE_group_set_number = 1
        if os.cpu_count() > 1:
            num_cpu = os.cpu_count() - 1

            print(f'    num_cpu: {num_cpu}')
        else:
            print('    num_cpu: 1')
            num_cpu = 1
            print('    your computer only have one CPU; unable to test multiprocessing function')

        print('    normalize: False')
        normalize = False

        revisit_threshold = RevisitThreshold(GetFiles_class_v = detail_vNE, GetFiles_class_i = data_file,
                                             tuple_t = tuple_t, tuple_u = tuple_u, tuple_l = tuple_l,
                                             output_file_name = output_file_name, num_cpu = num_cpu,
                                             normalize = normalize)

        revisit_threshold.current_vNE_group = []
        target = revisit_threshold.detail_vNE_group_set[current_vNE_group_set_number]
        for i in range(len(revisit_threshold.detail_vNE_group)):
            if revisit_threshold.detail_vNE_group[i] == target:
                revisit_threshold.current_vNE_group.append(revisit_threshold.detail_vNE_files[i])

        my_result = len(revisit_threshold.current_vNE_group)
        expected_result = 17
        self.assertEqual(my_result, expected_result)


        ##      1.2 group A
        print('        ---------------------------------------------------')
        print('             1.2: group A')
        print('        current_vNE_group_set_number: 0')
        current_vNE_group_set_number = 0

        revisit_threshold = RevisitThreshold(GetFiles_class_v = detail_vNE, GetFiles_class_i = data_file,
                                             tuple_t = tuple_t, tuple_u = tuple_u, tuple_l = tuple_l,
                                             output_file_name = output_file_name, num_cpu = num_cpu,
                                             normalize = normalize)

        revisit_threshold.current_vNE_group = []
        target = revisit_threshold.detail_vNE_group_set[current_vNE_group_set_number]
        for i in range(len(revisit_threshold.detail_vNE_group)):
            if revisit_threshold.detail_vNE_group[i] == target:
                revisit_threshold.current_vNE_group.append(revisit_threshold.detail_vNE_files[i])

        my_result = len(revisit_threshold.current_vNE_group)
        expected_result = 13
        self.assertEqual(my_result, expected_result)


        ## case 2: select the information-rich features based on different threshold
        #       2.1 keep the parameter the same as the time I first computed the information-rich feature
        print('        ---------------------------------------------------')
        print('        case 2: select the information-rich features based on different threshold')
        print('             2.1 keep the parameter the same as the time I first computed the information-rich feature')
        my_result = revisit_threshold.singleFile(current_vNE_group = revisit_threshold.current_vNE_group,
                                                 current_vNE_group_set_number = current_vNE_group_set_number,
                                                 current_u_level = 2, current_l_level = 2)

        expected_result = ['ASV_1', 'ASV_2', 'ASV_3', 'ASV_19', 'ASV_21', 'ASV_22', 'ASV_126']
        self.assertListEqual(my_result, expected_result)

        print('        ---------------------------------------------------')
        print('             2.2 change the parameter')
        #       2.2 change the parameter
        my_result = revisit_threshold.singleFile(current_vNE_group = revisit_threshold.current_vNE_group,
                                                 current_vNE_group_set_number = current_vNE_group_set_number,
                                                 current_u_level = 3, current_l_level = 3)

        expected_result = ['ASV_1', 'ASV_2', 'ASV_3', 'ASV_21']
        self.assertListEqual(my_result, expected_result)
        print('===========================================================')


    def test_singleGroup(self):
        print('\ntest_RevisitThreshold.singleGroup:')

        ## case 1: select the information-rich features based on different threshold
        #       1.1: keep the parameter the same as the time I first computed the information-rich feature
        print('        case 1: select the information-rich features based on different threshold')
        print('             1.1: keep the parameter the same as the time I first computed the information-rich feature')

        print('        -v: "emmer/data/retrospect_data_dir_2/detail_vNE/"]')
        args_v = 'emmer/data/retrospect_data_dir_2/detail_vNE/'
        input_dir = os.path.join(os.getcwd(), args_v)
        detail_vNE = GetFiles(input_dir = args_v)

        print('        -i: "emmer/data/retrospect_data_dir_2/pre_filter_data/"')
        args_i = 'emmer/data/retrospect_data_dir_2/pre_filter_data/'
        data_dir = os.path.join(os.getcwd(), args_i)
        data_file = GetFiles(input_dir = data_dir)

        print('        -t: "3,1,1"')
        args_t = '3,1,1'
        tuple_t = evaluateInputTuple(args_t)
        print('        -u: "3,1,1"')
        args_u = '3,1,1'
        tuple_u = evaluateInputTuple(args_u)
        print('        -l: "2,1,1')
        args_l = '2,1,1'
        tuple_l = evaluateInputTuple(args_l)
        print('        current_vNE_group_set_number: 0')
        current_vNE_group_set_number = 0
        print('        current_u_level: 2')
        current_u_level = 2
        print('        current_l_level: 2')
        current_l_level = 2
        print('        current_t_level: 2')
        current_t_level = 2
        print('        output_file_name: "test310.csv"')
        output_file_name = 'test310.csv'
        if os.cpu_count() > 1:
            num_cpu = os.cpu_count() - 1

            print(f'    num_cpu: {num_cpu}')
        else:
            print('    num_cpu: 1')
            num_cpu = 1
            print('    your computer only have one CPU; unable to test multiprocessing function')
        print('    normalize: False')
        normalize = False

        revisit_threshold = RevisitThreshold(GetFiles_class_v = detail_vNE, GetFiles_class_i = data_file,
                                             tuple_t = tuple_t, tuple_u = tuple_u, tuple_l = tuple_l,
                                             output_file_name = output_file_name, num_cpu = num_cpu,
                                             normalize = normalize)

        revisit_threshold.singleGroup(current_vNE_group_set_number = current_vNE_group_set_number,
                                      current_u_level = current_u_level, current_l_level = current_l_level,
                                      current_t_level = current_t_level)

        my_result = sorted(revisit_threshold.current_info_rich)
        expected_result = ['ASV_1', 'ASV_126', 'ASV_19', 'ASV_2', 'ASV_21', 'ASV_22', 'ASV_23', 'ASV_3', 'ASV_78']
        self.assertListEqual(my_result, expected_result)

        #       1.2 change the parameter
        print('        ---------------------------------------------------')
        print('             1.2 change the parameter')
        print('        current_u_level: 3')
        current_u_level = 3
        print('        current_l_level: 3')
        current_l_level = 3
        print('        current_t_level: 2')
        current_t_level = 2
        print('        output_file_name: "test333.csv"')
        output_file_name = 'test333.csv'

        revisit_threshold = RevisitThreshold(GetFiles_class_v = detail_vNE, GetFiles_class_i = data_file,
                                             tuple_t = tuple_t, tuple_u = tuple_u, tuple_l = tuple_l,
                                             output_file_name = output_file_name, num_cpu = num_cpu,
                                             normalize = normalize)

        revisit_threshold.singleGroup(current_vNE_group_set_number = current_vNE_group_set_number,
                                      current_u_level = current_u_level, current_l_level = current_l_level,
                                      current_t_level = current_t_level)

        my_result = sorted(revisit_threshold.current_info_rich)
        expected_result = ['ASV_1', 'ASV_126', 'ASV_2', 'ASV_21', 'ASV_3', 'ASV_78']
        self.assertListEqual(my_result, expected_result)
        print('===========================================================')


    def test_iteratesThroughGroupSet(self):
        print('\ntest_RevisitThreshold.iteratesThroughGroupSet:')

        ## Case 1: combine lists of information-rich features
        print('        Case 1: combine lists of information-rich features')
        print('        -v: "emmer/data/retrospect_data_dir_2/detail_vNE/"]')
        args_v = 'emmer/data/retrospect_data_dir_2/detail_vNE/'
        input_dir = os.path.join(os.getcwd(), args_v)
        detail_vNE = GetFiles(input_dir = args_v)
        print('        -i: "emmer/data/retrospect_data_dir_2/pre_filter_data/"')
        args_i = 'emmer/data/retrospect_data_dir_2/pre_filter_data/'
        data_dir = os.path.join(os.getcwd(), args_i)
        data_file = GetFiles(input_dir = data_dir)
        print('        -t: "2,1,1"')
        args_t = '2,1,1'
        tuple_t = evaluateInputTuple(args_t)
        print('        -u: "3,1,1"')
        args_u = '3,1,1'
        tuple_u = evaluateInputTuple(args_u)
        print('        -l: "3,1,1')
        args_l = '3,1,1'
        tuple_l = evaluateInputTuple(args_l)
        print('        current_u_level: 3')
        current_u_level = 3
        print('        current_l_level: 3')
        current_l_level = 3
        print('        current_t_level: 2')
        current_t_level = 2
        print('        output_file_name: "test377.csv"')
        output_file_name = 'test377.csv'
        if os.cpu_count() > 1:
            num_cpu = os.cpu_count() - 1

            print(f'    num_cpu: {num_cpu}')
        else:
            print('    num_cpu: 1')
            num_cpu = 1
            print('    your computer only have one CPU; unable to test multiprocessing function')

        print('    normalize: False')
        normalize = False

        revisit_threshold = RevisitThreshold(GetFiles_class_v = detail_vNE, GetFiles_class_i = data_file,
                                             tuple_t = tuple_t, tuple_u = tuple_u, tuple_l = tuple_l,
                                             output_file_name = output_file_name, num_cpu = num_cpu,
                                             normalize = normalize)

        revisit_threshold.iteratesThroughGroupSet(current_u_level = current_u_level,
                                                  current_l_level = current_l_level,
                                                  current_t_level = current_t_level)

        my_result = sorted(revisit_threshold.info_rich_at_current_threshold_level)
        expected_result = ['ASV_1', 'ASV_107', 'ASV_126', 'ASV_2', 'ASV_21', 'ASV_3', 'ASV_32', 'ASV_77', 'ASV_78']
        self.assertEqual(my_result, expected_result)

        ## Case 2: merge pre_filter data
        print('        ---------------------------------------------------')
        print('        Case 2: merge pre_filter data')
        my_result = revisit_threshold.merged_data.shape[1]
        expected_result = 1670
        self.assertEqual(my_result, expected_result)
        print('===========================================================')


    def test_compareBeforeAndAfterDataReduction(self):
        print('\ntest_RevisitThreshold.compareBeforeAndAfterDataReduction:')

        ## Case 1: check the number of information-rich feature
        print('    Case 1: check the number of information-rich feature')
        print('        -v: "emmer/data/retrospect_data_dir_2/detail_vNE/"]')
        args_v = 'emmer/data/retrospect_data_dir_2/detail_vNE/'
        input_dir = os.path.join(os.getcwd(), args_v)
        detail_vNE = GetFiles(input_dir = args_v)
        print('        -i: "emmer/data/retrospect_data_dir_2/pre_filter_data/"')
        args_i = 'emmer/data/retrospect_data_dir_2/pre_filter_data/'
        data_dir = os.path.join(os.getcwd(), args_i)
        data_file = GetFiles(input_dir = data_dir)
        print('        -u: "3,3,0"')
        args_u = '3,3,0'
        tuple_u = evaluateInputTuple(args_u)
        print('        -l: "3,3,0"')
        args_l = '3,3,0'
        tuple_l = evaluateInputTuple(args_l)
        print('        -t: "2,2,0"')
        args_t = '2,2,0'
        tuple_t = evaluateInputTuple(args_t)
        print('        output_file_name: "test427.csv"')
        output_file_name = 'test427.csv'
        print('    num_cpu: 1')
        num_cpu = 1
        print('    normalize: False')
        normalize = False

        revisit_threshold = RevisitThreshold(GetFiles_class_v = detail_vNE, GetFiles_class_i = data_file,
                                             tuple_t = tuple_t, tuple_u = tuple_u, tuple_l = tuple_l,
                                             output_file_name = output_file_name, num_cpu = num_cpu,
                                             normalize = normalize)
        revisit_threshold.iteratesThroughThresholdSetting()
        output = revisit_threshold.compareBeforeAndAfterDataReduction(current_row = 0)
        my_result = sorted(output[3])
        expected_result = ['ASV_1', 'ASV_107', 'ASV_126', 'ASV_2', 'ASV_21', 'ASV_3', 'ASV_32', 'ASV_77', 'ASV_78']
        self.assertListEqual(my_result, expected_result)


        ## Case 2: check data splitting
        print('        ---------------------------------------------------')
        print('        Case 2: check data splitting')
        my_result = revisit_threshold.current_non_info.shape[1] + revisit_threshold.current_info_rich.shape[1]
        expected_result = revisit_threshold.merged_data.shape[1]
        self.assertEqual(my_result, expected_result)


        ## Case 3: check procrustes test result
        print('        ---------------------------------------------------')
        print('        Case 3: check procrustes test result')
        my_result = output[4]
        expected_result = 0.005937139500067904
        numpy.testing.assert_almost_equal(my_result, expected_result, decimal = 5)
        os.remove('test427.csv')
        print('===========================================================')


    def test_iteratesThroughThresholdSetting(self):
        print('\ntest_RevisitThreshold.iteratesThroughThresholdSetting:')

        ## Case 1: Number of iteration
        print('        Case 1: Number of iteration')
        print('        -v: "emmer/data/retrospect_data_dir_2/detail_vNE/"]')
        args_v = 'emmer/data/retrospect_data_dir_2/detail_vNE/'
        input_dir = os.path.join(os.getcwd(), args_v)
        detail_vNE = GetFiles(input_dir = args_v)
        print('        -i: "emmer/data/retrospect_data_dir_2/pre_filter_data/"')
        args_i = 'emmer/data/retrospect_data_dir_2/pre_filter_data/'
        data_dir = os.path.join(os.getcwd(), args_i)
        data_file = GetFiles(input_dir = data_dir)
        print('        -t: "2,1,1"')
        args_t = '1,1,0'
        tuple_t = evaluateInputTuple(args_t)
        print('        -u: "4,2,1"')
        args_u = '3,2,1'
        tuple_u = evaluateInputTuple(args_u)
        print('        -l: "4,2,1')
        args_l = '3,2,1'
        tuple_l = evaluateInputTuple(args_l)
        print('        output_file_name: "test481.csv"')
        output_file_name = 'test481.csv'
        if os.cpu_count() > 1:
            num_cpu = os.cpu_count() - 1
            print(f'    num_cpu: {num_cpu}')
        else:
            print('    num_cpu: 1')
            num_cpu = 1
            print('    your computer only have one CPU; unable to test multiprocessing function')
        print('    normalize: False')
        normalize = False

        start_time = time.time()

        revisit_threshold = RevisitThreshold(GetFiles_class_v = detail_vNE, GetFiles_class_i = data_file,
                                             tuple_t = tuple_t, tuple_u = tuple_u, tuple_l = tuple_l,
                                             output_file_name = output_file_name, num_cpu = num_cpu,
                                             normalize = normalize)

        revisit_threshold.iteratesThroughThresholdSetting()

        my_result = revisit_threshold.iter_num
        expected_result = 4
        self.assertEqual(my_result, expected_result)
        print('Speed test for RevisitThreshold.iteratesThroughThresholdSetting')
        print('computation time: %s seconds ' % (time.time() - start_time))
        os.remove('test481.csv')


        ## Case 2: Ability to include NaN
        print('        ---------------------------------------------------')
        print('        Case 2: Ability to include NaN')
        print('        -t: "2,1,1"')
        args_t = '2,1,1'
        tuple_t = evaluateInputTuple(args_t)
        print('        -u: "30,29,1"')
        args_u = '30,29,1'
        tuple_u = evaluateInputTuple(args_u)
        print('        -l: "30,29,1')
        args_l = '30,29,1'
        tuple_l = evaluateInputTuple(args_l)
        print('        output_file_name: "test509.csv"')
        output_file_name = 'test509.csv'
        if os.cpu_count() > 1:
            num_cpu = os.cpu_count() - 1

            print(f'    num_cpu: {num_cpu}')
        else:
            print('    num_cpu: 1')
            num_cpu = 1
            print('    your computer only have one CPU; unable to test multiprocessing function')

        print('    normalize: False')
        normalize = False

        revisit_threshold = RevisitThreshold(GetFiles_class_v = detail_vNE, GetFiles_class_i = data_file,
                                             tuple_t = tuple_t, tuple_u = tuple_u, tuple_l = tuple_l,
                                             output_file_name = output_file_name, num_cpu = num_cpu,
                                             normalize = normalize)

        revisit_threshold.iteratesThroughThresholdSetting()
        my_result = list(revisit_threshold.threshold_setting_result['info_to_ori_disparity'].isnull())

        expected_result = [True, True, True, True, True, True, True, True]
        self.assertEqual(my_result, expected_result)

        my_result = revisit_threshold.threshold_setting_result['non_info_to_ori_disparity'].iloc[0]
        expected_result = 0
        numpy.testing.assert_almost_equal(my_result, expected_result)

        os.remove('test509.csv')
        print('===========================================================')


    def test_compareSettings(self):
        print('\ntest_RevisitThreshold.compareSettings:')
        print('        Case 1: Expected input threshold setting')
        print('        -v: "emmer/data/retrospect_data_dir_2/detail_vNE/"]')
        args_v = 'emmer/data/retrospect_data_dir_2/detail_vNE/'
        input_dir = os.path.join(os.getcwd(), args_v)
        detail_vNE = GetFiles(input_dir = args_v)
        print('        -i: "emmer/data/retrospect_data_dir_2/pre_filter_data/"')
        args_i = 'emmer/data/retrospect_data_dir_2/pre_filter_data/'
        data_dir = os.path.join(os.getcwd(), args_i)
        data_file = GetFiles(input_dir = data_dir)
        print('        -t: "1,1,0"')
        args_t = '1,1,0'
        tuple_t = evaluateInputTuple(args_t)
        print('        -u: "3,2,1"')
        args_u = '3,2,1'
        tuple_u = evaluateInputTuple(args_u)
        print('        -l: "3,2,1')
        args_l = '3,2,1'
        tuple_l = evaluateInputTuple(args_l)
        print('        output_file_name: "test570.csv"')
        output_file_name = 'test570.csv'
        print('    num_cpu: 1')  # order matters in this case
        num_cpu = 1
        print('    normalize: False')
        normalize = False

        revisit_threshold = RevisitThreshold(GetFiles_class_v = detail_vNE, GetFiles_class_i = data_file,
                                             tuple_t = tuple_t, tuple_u = tuple_u, tuple_l = tuple_l,
                                             output_file_name = output_file_name, num_cpu = num_cpu,
                                             normalize = normalize)

        revisit_threshold.iteratesThroughThresholdSetting()
        revisit_threshold.compareSettings()

        my_result = revisit_threshold.selected['u']
        expected_result = 2
        numpy.testing.assert_almost_equal(my_result, expected_result)

        my_result = revisit_threshold.selected['l']
        expected_result = 2

        numpy.testing.assert_almost_equal(my_result, expected_result)

        my_result = revisit_threshold.selected['t']
        expected_result = 1
        numpy.testing.assert_almost_equal(my_result, expected_result)

        os.remove('test570.csv')


        print('        ---------------------------------------------------')
        print('        Case 2: No information-rich feature can be selected at the input threshold setting')
        print('        -t: "2,1,1"')
        args_t = '2,1,1'
        tuple_t = evaluateInputTuple(args_t)
        print('        -u: "30,29,1"')
        args_u = '30,29,1'
        tuple_u = evaluateInputTuple(args_u)
        print('        -l: "30,29,1')
        args_l = '30,29,1'
        tuple_l = evaluateInputTuple(args_l)
        print('        output_file_name: "test605.csv"')
        output_file_name = 'test605.csv'
        if os.cpu_count() > 1:
            num_cpu = os.cpu_count() - 1

            print(f'    num_cpu: {num_cpu}')
        else:
            print('    num_cpu: 1')
            num_cpu = 1
            print('    your computer only have one CPU; unable to test multiprocessing function')
        print('    normalize: False')
        normalize = False

        with self.assertRaises(ErrorCode27):
            revisit_threshold = RevisitThreshold(GetFiles_class_v = detail_vNE, GetFiles_class_i = data_file,
                                                 tuple_t = tuple_t, tuple_u = tuple_u, tuple_l = tuple_l,
                                                 output_file_name = output_file_name, num_cpu = num_cpu,
                                                 normalize = normalize, suppress = True)

            revisit_threshold.iteratesThroughThresholdSetting()
            out = revisit_threshold.compareSettings()

        os.remove('test605.csv')
        print('===========================================================')


if __name__ == '__main__':
    unittest.main()
