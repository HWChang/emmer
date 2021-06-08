#!/usr/bin/env python3

## usage
# at a level above emmer/
# python3 -m emmer.test.test_bake

from ..main.advanced.iteration import MinusOneVNE, InfoRichCalling, reproducibility_summary
from ..main.basic.read import RawDataImport, RetrospectDataImport, GetFiles
from ..bake import BakeCommonArgs

import argparse
import unittest
import sys


class TestBakeCommonArgs(unittest.TestCase):

    def test_getArgsM(self):
        print('\ntest_TestBakeCommonArgs.getArgsM:')
        print('        case 1: error handling')
        print('             1.1: missing args.m setting')
        sys.argv[1:] = []
        #with self.assertRaises(ErrorCode9):
        #    processed_args = BakeCommonArgs(suppress = True)
        #    processed_args.getArgsM()
        processed_args = BakeCommonArgs(suppress = False, test = True, neglect = True, silence = False)
        processed_args.getArgsM()
        my_result = processed_args.warning_code
        expected_result = '9'
        self.assertEqual(my_result, expected_result)

        print('        ---------------------------------------------------')
        print('             1.2: unexpected args.m setting')
        sys.argv[1:] = ['-m', 'Unknown_mode']
        #with self.assertRaises(ErrorCode9):
        #    processed_args = BakeCommonArgs(suppress = True)
        #    processed_args.getArgsM()
        processed_args = BakeCommonArgs(suppress = False, test = True, neglect = True, silence = False)
        processed_args.getArgsM()
        my_result = processed_args.warning_code
        expected_result = '9'
        self.assertEqual(my_result, expected_result)

        print('===========================================================')


    def test_getHomeKeepingArgs(self):
        print('\ntest_TestBakeCommonArgs.getHomeKeepingArgs:')
        print('        case 1: get arguments')
        sys.argv[1:] = ['-m', 'Reproducibility']
        processed_args = BakeCommonArgs(suppress = True, test = False, neglect = True, silence = False)
        processed_args.getHomeKeepingArgs()

        my_result = processed_args.selected_model
        expected_result = 'Reproducibility'

        self.assertEqual(my_result, expected_result)
        print('===========================================================')


if __name__ == '__main__':
    unittest.main()
