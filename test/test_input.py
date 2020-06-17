#!/usr/bin/env python3

## usage
# at a level above emmer/
# python3 -m emmer.test.test_input

from ..troubleshoot.err.error import ErrorCode7, ErrorCode9, ErrorCode10, ErrorCode28, ErrorCode31, ErrorCode33, ErrorCode36, ErrorCode37
from ..troubleshoot.inquire.input import EvaluateInput

from unittest.mock import patch
import unittest


class TestEvaluateInput(unittest.TestCase):

    def test_EvaluateInput(self):
        print('\ntest_EvaluateInput:')
        print('        case 1: raise error when the number of elements in input does not the match expecation')
        with self.assertRaises(ErrorCode10):
            confirmed_input = EvaluateInput(input = ['A', 'B', 'unexpected_additional_element'],
                                            set = ['correpsonding_to_A', 'correpsonding_to_B'],
                                            suppress = True, expect = 0)
        print('===========================================================')


    def test_evaluateOption(self):
        print('\ntest_EvaluateInput.evaluateModeOption:')
        print('        case 1: missing expect argument')
        with self.assertRaises(ErrorCode7):
            confirmed_input = EvaluateInput(input = ['A', 'B'], set = ['correpsonding_to_A', 'correpsonding_to_B'],
                                            suppress = True, expect = 0)
            confirmed_input.evaluateModeOption()


        print('        ---------------------------------------------------')
        print('        case 2: unexpected input')

        expected_dict = {'1': 'Individual',
                         '2': 'Permanova',
                         '3': 'RevisitThreshold',
                         '4': 'Reproducibility',
                         '5': 'Bifurication'}

        print('             2.1: unexpected option number')
        with self.assertRaises(ErrorCode9):
            confirmed_input = EvaluateInput(input = ['9999'], set = ['mode'],
                                            suppress = True, expect = expected_dict)
            confirmed_input.evaluateModeOption()
        #confirmed_input = EvaluateInput(input = ['9999'], set = ['mode'],
        #                                suppress = True, expect = expected_dict)
        #confirmed_input.evaluateModeOption()
        #my_result = processed_args.warning_code
        #expected_result = '9'
        #self.assertEqual(my_result, expected_result)

        print('        ---------------------------------------------------')
        print('             2.2: unexpected option number')
        with self.assertRaises(ErrorCode9):
            confirmed_input = EvaluateInput(input = ['individual'], set = ['mode'],
                                            suppress = True, expect = expected_dict)
            confirmed_input.evaluateModeOption()
        #confirmed_input = EvaluateInput(input = ['individual'], set = ['mode'],
        #                                suppress = True, expect = expected_dict)
        #confirmed_input.evaluateModeOption()
        #my_result = processed_args.warning_code
        #expected_result = '9'
        #self.assertEqual(my_result, expected_result)

        print('        ---------------------------------------------------')
        print('             3: expected to work')
        print('             3.1: output dictionary')
        confirmed_input = EvaluateInput(input = ['Individual'], set = ['mode'],
                                        suppress = True, expect = expected_dict)
        confirmed_input.evaluateModeOption()

        my_result = confirmed_input.map_input
        expected_result = {'mode': 'Individual'}
        self.assertEqual(my_result, expected_result)


        print('        ---------------------------------------------------')
        print('             3.2: pass token')
        my_result = confirmed_input.passed
        expected_result = True
        self.assertEqual(my_result, expected_result)
        print('===========================================================')


    def test_evaluateColor(self):
        print('\ntest_EvaluateInput.evaluateColor:')
        print('        case 1: EvaluateInput.expect should remain as default')
        with self.assertRaises(ErrorCode31):
            confirmed_input = EvaluateInput(input = ['red', 'blue'], set = ['correpsonding_to_A', 'correpsonding_to_B'],
                                            suppress = True, expect = 'not_default')
            confirmed_input.evaluateColor()


        print('        ---------------------------------------------------')
        print('        case 2: not in mcolors.cnames.keys() or none or hex color')
        print('             2.1: not in mcolors.cnames.keys()')
        with self.assertRaises(ErrorCode28):
            confirmed_input = EvaluateInput(input = ['re', 'blue'], set = ['correpsonding_to_A', 'correpsonding_to_B'],
                                            suppress = True, expect = 0)
            confirmed_input.evaluateColor()


        print('        ---------------------------------------------------')
        print('             2.1: not in hex color')
        with self.assertRaises(ErrorCode28):
            confirmed_input = EvaluateInput(input = ['red', '#ZZZZZZ'], set = ['correpsonding_to_A', 'correpsonding_to_B'],
                                            suppress = True, expect = 0)
            confirmed_input.evaluateColor()


        print('        ---------------------------------------------------')
        print('        case 3: expect to work')
        print('             3.1: in mcolors.cnames.keys()')
        confirmed_input = EvaluateInput(input = ['red', 'blue'], set = ['correpsonding_to_A', 'correpsonding_to_B'],
                                        suppress = True, expect = 0)
        confirmed_input.evaluateColor()

        my_result = confirmed_input.passed
        expected_result = True
        self.assertEqual(my_result, expected_result)


        print('        ---------------------------------------------------')
        print('             3.1: in none')
        confirmed_input = EvaluateInput(input = ['none', 'none'], set = ['correpsonding_to_A', 'correpsonding_to_B'],
                                        suppress = True, expect = 0)
        confirmed_input.evaluateColor()

        my_result = confirmed_input.passed
        expected_result = True
        self.assertEqual(my_result, expected_result)


        print('        ---------------------------------------------------')
        print('             3.2: in hex color')
        confirmed_input = EvaluateInput(input = ['#ff0000', '#0000FF'], set = ['correpsonding_to_A', 'correpsonding_to_B'],
                                        suppress = True, expect = 0)
        confirmed_input.evaluateColor()

        my_result = confirmed_input.passed
        expected_result = True
        self.assertEqual(my_result, expected_result)
        print('===========================================================')


    def test_evaluateStatCluster(self):
        print('\ntest_EvaluateInput.evaluateStatCluster:')
        print('        case 1: EvaluateInput.expect should remain as default')
        with self.assertRaises(ErrorCode31):
            confirmed_input = EvaluateInput(input = ['A', 'B'], set = ['correpsonding_to_A', 'correpsonding_to_B'],
                                            suppress = True, expect = 'not_default')
            confirmed_input.evaluateStatCluster()


        print('        ---------------------------------------------------')
        print('        case 2: only one cluster was given')
        with self.assertRaises(ErrorCode37):
            confirmed_input = EvaluateInput(input = ['A', 'A'], set = ['correpsonding_to_A', 'correpsonding_to_B'],
                                            suppress = True, expect = 0)
            confirmed_input.evaluateStatCluster()


        print('        ---------------------------------------------------')
        print('        case 3: expect to work')
        confirmed_input = EvaluateInput(input = ['A', 'B'], set = ['correpsonding_to_A', 'correpsonding_to_B'],
                                        suppress = True, expect = 0)
        confirmed_input.evaluateStatCluster()

        my_result = confirmed_input.passed
        expected_result = True
        self.assertEqual(my_result, expected_result)
        print('===========================================================')


    def test_evaluateMarker(self):
        print('\ntest_EvaluateInput.evaluateMarker:')
        print('        case 1: EvaluateInput.expect should remain as default')
        with self.assertRaises(ErrorCode31):
            confirmed_input = EvaluateInput(input = ['A', 'B'], set = ['correpsonding_to_A', 'correpsonding_to_B'],
                                            suppress = True, expect = 'not_default')
            confirmed_input.evaluateMarker()


        print('        ---------------------------------------------------')
        print('        case 2: not a marker')
        with self.assertRaises(ErrorCode33):
            confirmed_input = EvaluateInput(input = ['not_a_marker_A', 'not_a_marker_B'], set = ['correpsonding_to_A', 'correpsonding_to_B'],
                                            suppress = True, expect = 0)
            confirmed_input.evaluateMarker()



        print('        ---------------------------------------------------')
        print('        case 3: expect to work')
        confirmed_input = EvaluateInput(input = ['o', 'H'], set = ['correpsonding_to_A', 'correpsonding_to_B'],
                                        suppress = True, expect = 0)
        confirmed_input.evaluateMarker()

        my_result = confirmed_input.passed
        expected_result = True
        self.assertEqual(my_result, expected_result)
        print('===========================================================')


    def test_evaluateGroupOption(self):
        print('\ntest_EvaluateInput.evaluateGroupOption:')
        print('        case 1: missing expect argument')
        with self.assertRaises(ErrorCode7):
            confirmed_input = EvaluateInput(input = ['A', 'B'], set = ['correpsonding_to_A', 'correpsonding_to_B'],
                                            suppress = True, expect = 0)
            confirmed_input.evaluateGroupOption()


        print('        ---------------------------------------------------')
        print('        case 2: unexpected input')

        expected_dict = {'1': 'Group',
                         '2': 'Individual'}

        print('             2.1: unexpected option number')
        with self.assertRaises(ErrorCode36):
            confirmed_input = EvaluateInput(input = ['9999'], set = ['color_by'],
                                            suppress = True, expect = expected_dict)
            confirmed_input.evaluateGroupOption()


        print('        ---------------------------------------------------')
        print('             2.2: unexpected option number')
        with self.assertRaises(ErrorCode36):
            confirmed_input = EvaluateInput(input = ['individual'], set = ['color_by'],
                                            suppress = True, expect = expected_dict)
            confirmed_input.evaluateGroupOption()


        print('        ---------------------------------------------------')
        print('             3: expected to work')
        print('             3.1: output dictionary')
        confirmed_input = EvaluateInput(input = ['Individual'], set = ['color_by'],
                                        suppress = True, expect = expected_dict)
        confirmed_input.evaluateGroupOption()

        my_result = confirmed_input.map_input
        expected_result = {'color_by': 'Individual'}
        self.assertEqual(my_result, expected_result)
        print('===========================================================')


# https://stackoverflow.com/questions/21046717/python-mocking-raw-input-in-unittests

if __name__ == '__main__':
    unittest.main()
