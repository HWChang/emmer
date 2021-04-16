#!/usr/bin/env python3

## usage
# at a level above emmer/
# python3 -m emmer.test.test_individual

from ..bake import BakeCommonArgs
from ..main.basic.read import RetrospectDataImport, GetFiles
from ..posthoc.visual.individual import IndividualArgs
from ..troubleshoot.err.error import Error, ErrorCode8

import unittest
import sys
import os


class TestIndividualArgs(unittest.TestCase):

    def test_IndividualArgs(self):
        print('\ntest_IndividualArgs:')
        print('        case 1: error handling')
        print('             1.1: missing args.i')
        sys.argv[1:] = ['-m', 'Individual']
        current_wd = os.getcwd()
        processed_args = BakeCommonArgs(suppress = True, test = False, neglect = True, silence = False)
        processed_args.getHomeKeepingArgs()

        with self.assertRaises(ErrorCode8):
            individual_args = IndividualArgs(args = processed_args.args, current_wd = current_wd,
                                             suppress = True, silence = False)


        print('        ---------------------------------------------------')
        print('             1.2: giving both args.i and args.p')
        sys.argv[1:] = ['-m', 'Individual', '-p', 'emmer/data/bake_data_dir_7/_retrospect_individaul_coloring_parameter.csv',
                        '-i', 'emmer/data/bake_data_dir_6/filtered_infoRich__PCA_coordinates.csv']
        current_wd = os.getcwd()
        processed_args = BakeCommonArgs(suppress = True, test = False, neglect = True, silence = False)
        processed_args.getHomeKeepingArgs()

        #with self.assertRaises(WarningCode13):
        individual_args = IndividualArgs(args = processed_args.args, current_wd = current_wd,
                                         suppress = True, silence = False)
        my_result = individual_args.warning_code
        expected_result = '13'
        self.assertEqual(my_result, expected_result)


        print('        ---------------------------------------------------')
        print('             1.3: args.i is not a csv file')
        sys.argv[1:] = ['-m', 'Individual', '-i', 'emmer/data/problem_maker/read_module/not_a_csv_file.txt']
        current_wd = os.getcwd()
        processed_args = BakeCommonArgs(suppress = True, test = False, neglect = True, silence = False)
        processed_args.getHomeKeepingArgs()

        with self.assertRaises(ErrorCode8):
            individual_args = IndividualArgs(args = processed_args.args, current_wd = current_wd,
                                             suppress = True, silence = False)


        print('        ---------------------------------------------------')
        print('        case 2: expect to work')
        sys.argv[1:] = ['-m', 'Individual', '-p', 'emmer/data/bake_data_dir_7/_retrospect_individaul_coloring_parameter.csv']
        current_wd = os.getcwd()
        processed_args = BakeCommonArgs(suppress = True, test = False, neglect = True, silence = False)
        processed_args.getHomeKeepingArgs()

        individual_args = IndividualArgs(args = processed_args.args, current_wd = current_wd,
                                         suppress = True, silence = False)
        print(type(individual_args))
        print(individual_args.pca_coordinate.coordinate_w_info.shape)
        print('===========================================================')

if __name__ == '__main__':
    unittest.main()
