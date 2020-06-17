#!/usr/bin/env python3

## usage:
# at a level above emmer/
# python3 -m emmer.test.test_technical

from ..troubleshoot.err.error import ErrorCode23
from ..toolbox.technical import *
import unittest
import numpy as np
import pandas as pd
import sys


class TestFlattern(unittest.TestCase):

    def test_flattern(self):
        print('\ntest_flattern:')
        print('        list_of_list = [[1, 2], [3, 4]]')
        list_of_list = [[1, 2], [3, 4]]

        my_result = flattern(list_of_list)
        expected_result = [1, 2, 3, 4]
        self.assertListEqual(my_result, expected_result)
        print('===========================================================')


class TestEmptyNumpyArray(unittest.TestCase):

    def test_emptyNumpyArray(self):
        print('\ntest_emptyNumpyArray:')
        print('        Case 1: confirm the function generate a empty array')
        print('        nrow = 3')
        nrow = 3
        print('        ncol = 4')
        ncol = 4

        np_array = emptyNumpyArray(nrow = 3, ncol = 4)

        ## Case 1: confirm the function generate a empty array
        df = pd.DataFrame(data = np_array)
        my_result = sum(flattern(df.isnull().values.tolist()))
        expected_result = 12
        self.assertEqual(my_result, expected_result)

        ## Case 2: confirm deminsion
        print('        ---------------------------------------------------')
        print('        Case 2: confirm deminsion')
        my_result = df.shape[0]
        expected_result = 3
        self.assertEqual(my_result, expected_result)
        print('===========================================================')


class TestToFloat(unittest.TestCase):

    def test_toFloat(self):
        print('\ntest_toFloat:')
        print('        Case 1: match expected input')
        print('        number_in_str = 9')
        number_in_str = 9

        ## Case 1: match expected input
        my_result = toFloat(number_in_str, suppress = False)
        expected_result = 9
        self.assertEqual(my_result, expected_result)

        ## Case 2: unexpected input; arise error msg
        print('        ---------------------------------------------------')
        print('        Case 2: unexpected input; arise error message')
        print('        number_in_str = "A"')
        number_in_str = 'A'

        with self.assertRaises(ErrorCode23):
            output = toFloat(number_in_str, suppress = True)
        print('===========================================================')


class TestFloatRange(unittest.TestCase):

    def test_floatRange(self):
        ## Case 1: normal input
        print('\ntest_floatRange:')
        print('        Case 1: normal input')
        print('        input_tuple = (3, 1, 0.5)')
        input_tuple = (3, 1, 0.5)

        my_result = floatRange(input_tuple)
        expected_result = [1, 1.5, 2, 2.5, 3]
        self.assertEqual(my_result, expected_result)

        ## Case 2: max == min
        print('        ---------------------------------------------------')
        print('        Case 2: max == min')
        print('        input_tuple = (2, 2, 0)')
        input_tuple = (2, 2, 0)

        my_result = floatRange(input_tuple)
        expected_result = [2]
        self.assertEqual(my_result, expected_result)
        print('===========================================================')


class TestAddElementsInList(unittest.TestCase):

    def test_addElementsInList(self):
        print('\ntest_addElementsInList:')
        print('        list_1 = [1, 2, 3]')
        list_1 = [1, 2, 3]
        print('        list_2 = [3, 2, 1]')
        list_2 = [3, 2, 1]

        my_result = addElementsInList(list_1 = list_1, list_2 = list_2)
        expected_result = [4, 4, 4]
        self.assertEqual(my_result, expected_result)
        print('===========================================================')


class TestDualAssignment(unittest.TestCase):

    def test_dualAssignment(self):
        print('\ntest_addElementsInList:')
        print('        dataframe = pd.DataFrame([[1,2,3,4],[2,3,2,3],[1,3,2,4]], columns = ["A", "A-B", "B", "A-C"])')
        dataframe = pd.DataFrame([[1,2,3,4],[2,3,2,3],[1,3,2,4]], columns = ["A", "A-B", "B", "A-C"])
        print('        sep = "-"')
        sep = "-"

        print(dataframe)
        my_result = dualAssignment(dataframe = dataframe, sep = sep)
        print(my_result)
        expected_result = {'A': [7, 8, 8], 'B': [5, 5, 5], 'C': [4, 3, 4]}
        self.assertEqual(my_result, expected_result)
        print('===========================================================')
        

if __name__ == '__main__':
    unittest.main()
