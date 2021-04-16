#!/usr/bin/env python3

## usage
# at a level above emmer/
# python3 -m emmer.test.test_reproducibility

from ..bake import BakeCommonArgs
from ..main.basic.read import RetrospectDataImport, GetFiles
from ..posthoc.stats.reproducibility import ReproducibilitySummary, ReproducibilityArgs
from ..troubleshoot.err.error import *
from ..troubleshoot.warn.warning import *

import unittest
import numpy
import sys
import os

class TestReproducibilityArgs(unittest.TestCase):

    def test_ReproducibilityArgs(self):
        print('\ntest_ReproducibilityArgs:')
        print('        case 1: missing args.b setting')
        sys.argv[1:] = ['-m', 'Reproducibility', '-i', 'emmer/data/bake_data_dir_4/information_rich_features_summary.csv']
        current_wd = os.getcwd()
        processed_args = BakeCommonArgs(suppress = True, test = False, neglect = True, silence = False)
        processed_args.getHomeKeepingArgs()
        reproducibility_args = ReproducibilityArgs(args = processed_args.args, current_wd = current_wd,
        	                                       suppress = True, silence = False)
        my_result = reproducibility_args.warning_code
        expected_result = '7'
        self.assertEqual(my_result, expected_result)


        print('        ---------------------------------------------------')
        print('        case 3: missing args.i setting')
        sys.argv[1:] = ['-m', 'Reproducibility', '-b', '40']
        current_wd = os.getcwd()
        processed_args = BakeCommonArgs(suppress = True, test = False, neglect = True, silence = False)
        processed_args.getHomeKeepingArgs()
        with self.assertRaises(ErrorCode1):
            reproducibility_args = ReproducibilityArgs(args = processed_args.args, current_wd = current_wd,
                                                       suppress = True, silence = False)
            reproducibility_args.getArgsI()


        print('        ---------------------------------------------------')
        print('        case 4: expect to work')
        print('             4.1: single file')
        sys.argv[1:] = ['-m', 'Reproducibility', '-b', '40', '-i', 'emmer/data/bake_data_dir_4/information_rich_features_summary.csv']
        processed_args = BakeCommonArgs(suppress = True, test = False, neglect = True, silence = False)
        current_wd = os.getcwd()
        processed_args.getHomeKeepingArgs()
        reproducibility_args = ReproducibilityArgs(args = processed_args.args, current_wd = current_wd,
                                                   suppress = True, silence = False)

        my_result = numpy.mean(reproducibility_args.reproducibility_list)
        expected_result = 88.4877777777778
        self.assertAlmostEqual(my_result, expected_result)


        print('        ---------------------------------------------------')
        print('             4.1.1: handle bin_num')
        my_result = reproducibility_args.bin_num
        expected_result = 40
        self.assertEqual(my_result, expected_result)


        print('        ---------------------------------------------------')
        print('             4.2: multiple files')
        print('             4.2.1: summarized reproducibilty output')
        sys.argv[1:] = ['-m', 'Reproducibility', '-b', '20', '-i', 'emmer/data/bake_data_dir_5']
        current_wd = os.getcwd()
        processed_args = BakeCommonArgs(suppress = True, test = False, neglect = True, silence = False)
        processed_args.getHomeKeepingArgs()
        reproducibility_args = ReproducibilityArgs(args = processed_args.args, current_wd = current_wd,
                                                       suppress = True, silence = False)
        my_result = numpy.mean(reproducibility_args.reproducibility_list)
        expected_result = 88.7938888888889
        self.assertAlmostEqual(my_result, expected_result)

        print('        ---------------------------------------------------')
        print('             4.2.2: reproducibilty output from a single input file')
        sys.argv[1:] = ['-m', 'Reproducibility', '-b', '20', '-i', 'emmer/data/bake_data_dir_8/case2_in_folder/']
        current_wd = os.getcwd()
        processed_args = BakeCommonArgs(suppress = True, test = False, neglect = True, silence = False)
        processed_args.getHomeKeepingArgs()
        reproducibility_args = ReproducibilityArgs(args = processed_args.args, current_wd = current_wd,
                                                       suppress = True, silence = False)

        my_result = numpy.mean(reproducibility_args.reproducibility_list)
        expected_result = 79.1666666671568
        self.assertAlmostEqual(my_result, expected_result)

        print('        ---------------------------------------------------')
        print('             4.3: generate a summarizing dataframe if there are multiple input file')
        print('                  row: information-rich features; column: input file names')
        sys.argv[1:] = ['-m', 'Reproducibility', '-b', '20', '-i', 'emmer/data/bake_data_dir_8/case3_in_folder/']
        current_wd = os.getcwd()
        processed_args = BakeCommonArgs(suppress = True, test = False, neglect = True, silence = False)
        processed_args.getHomeKeepingArgs()
        reproducibility_args = ReproducibilityArgs(args = processed_args.args, current_wd = current_wd,
                                                   suppress = True, silence = False)
        my_result = reproducibility_args.reproducibility_summary_df.shape[0]
        expected_result = 9
        self.assertEqual(my_result, expected_result)
        print('===========================================================')


class TestReproducibility(unittest.TestCase):

    def test_FatternInput(self):
        print('\ntest_Reproducibility.FatternInput:')
        print('    -i: "emmer/data/retrospect_data_dir_1/information_rich_features_summary.csv"')
        input_dir = 'emmer/data/retrospect_data_dir_1/information_rich_features_summary.csv'
        print('    -s: "reproducibility"')
        style = 'reproducibility'

        current_wd = os.getcwd()
        repro = RetrospectDataImport(file_name = os.path.join(current_wd, input_dir), type = style)
        repro_summary = ReproducibilitySummary(repro.reproducibility)

        my_result = list(repro_summary.reproducibility[0:6])

        expected_result = [100.0, 94.12, 0.0, 11.76, 0.0, 100.0]
        self.assertListEqual(my_result, expected_result)
        print('===========================================================')


    def test_RemoveZero(self):
        print('\ntest_Reproducibility.RemoveZero:')
        print('        case 1: post-removal result')
        print('             1.1: check the value of elements that are keep after the removal')
        print('    -i: "emmer/data/retrospect_data_dir_1/information_rich_features_summary.csv"')
        input_dir = 'emmer/data/retrospect_data_dir_1/information_rich_features_summary.csv'
        print('    -s: "reproducibility"')
        style = 'reproducibility'

        current_wd = os.getcwd()
        repro = RetrospectDataImport(file_name = os.path.join(current_wd, input_dir), type = style)
        repro_summary = ReproducibilitySummary(repro.reproducibility)

        # test 1
        my_result = list(repro_summary.reproducibility_no_zero[0:6])
        expected_result = [100.0, 94.12, 11.76, 100.0, 84.62, 100.0]
        self.assertListEqual(my_result, expected_result)


        # test 2
        print('        ---------------------------------------------------')
        print('             1.2: check the number of elements that are keep after the removal')
        my_result = len(repro_summary.reproducibility_no_zero)
        expected_result = 20
        self.assertEqual(my_result, expected_result)
        print('===========================================================')


    def test_Stat(self):
        print('\ntest_Reproducibility.Stat:')
        print('        case 1: result')
        print('    -i: "emmer/data/retrospect_data_dir_1/information_rich_features_summary.csv"')
        input_dir = 'emmer/data/retrospect_data_dir_1/information_rich_features_summary.csv'
        print('    -s: "reproducibility"')
        style = 'reproducibility'

        current_wd = os.getcwd()
        repro = RetrospectDataImport(file_name = os.path.join(current_wd, input_dir), type = style)
        repro_summary = ReproducibilitySummary(repro.reproducibility)

        # test 1
        print('             1.1: median')
        my_result = numpy.median(repro_summary.reproducibility_no_zero)
        expected_result = 84.62
        numpy.testing.assert_almost_equal(my_result, expected_result)


        # test 2
        print('        ---------------------------------------------------')
        print('             1.2: mean')
        my_result = numpy.mean(repro_summary.reproducibility_no_zero)
        expected_result = 75.95150000000001
        numpy.testing.assert_almost_equal(my_result, expected_result)


        # test 3
        print('        ---------------------------------------------------')
        print('             1.3: standard deviation')
        my_result = numpy.std(repro_summary.reproducibility_no_zero)
        expected_result = 28.751601916241118
        numpy.testing.assert_almost_equal(my_result, expected_result)
        print('===========================================================')


if __name__ == '__main__':
    unittest.main()
