#!/usr/bin/env python3

## usage
# at a level above emmer/
# python3 -m emmer.test.test_permanova

from ..bake import BakeCommonArgs
from ..main.basic.read import RetrospectDataImport, GetFiles
from ..posthoc.stats.permanova import PermanovaArgs, permanovaResult
from ..troubleshoot.err.error import *
#from ..troubleshoot.warn.warning import *

import unittest
import numpy
import sys
import os

class TestPermanovaArgs(unittest.TestCase):

    def test_PermanovaArgs(self):
        print('\ntest_PermanovaArgs:')
        print('        case 1: error and warning handling')
        print('             1.1: give both args.i and args.p')
        sys.argv[1:] = ['-m', 'Permanova', '-i', 'emmer/data/bake_data_dir_6/filtered_infoRich__PCA_coordinates.csv',
                        '-p', 'emmer/data/bake_data_dir_6/_retrospect_permanova_parameter.csv']
        current_wd = os.getcwd()
        processed_args = BakeCommonArgs(suppress = True, test = False, neglect = True, silence = False)
        processed_args.getHomeKeepingArgs()

        permanova_args = PermanovaArgs(args = processed_args.args, current_wd = current_wd,
         	                           suppress = True, silence = False)
        my_result = permanova_args.warning_code
        expected_result = '13'
        self.assertEqual(my_result, expected_result)

        print('        ---------------------------------------------------')
        print('             1.2: no args.i nor args.p')
        sys.argv[1:] = ['-m', 'Permanova']
        current_wd = os.getcwd()
        processed_args = BakeCommonArgs(suppress = True, test = False, neglect = True, silence = False)
        processed_args.getHomeKeepingArgs()

        with self.assertRaises(ErrorCode8):
            permanova_args = PermanovaArgs(args = processed_args.args, current_wd = current_wd,
            	                           suppress = True, silence = False)

        print('        ---------------------------------------------------')
        print('        case 2: expect to work')
        sys.argv[1:] = ['-m', 'Permanova', '-p', 'emmer/data/bake_data_dir_6/_retrospect_permanova_parameter.csv']
        current_wd = os.getcwd()
        processed_args = BakeCommonArgs(suppress = True, test = False, neglect = True, silence = False)
        processed_args.getHomeKeepingArgs()

        permanova_args = PermanovaArgs(args = processed_args.args, current_wd = current_wd,
            	                       suppress = True, silence = False)

        my_restul = len(permanova_args.cluster)
        expected_result = 30

        self.assertEqual(my_restul, expected_result)
        print('===========================================================')


if __name__ == '__main__':
    unittest.main()
