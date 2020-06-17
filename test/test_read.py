#!/usr/bin/env python3

## usage
# at a level above emmer/
# python3 -m emmer.test.test_read

from ..main.basic.read import RawDataImport, GetFiles, MergeTargetedFiles, RetrospectDataImport
from ..troubleshoot.err.error import ErrorCode1, ErrorCode9, ErrorCode11, ErrorCode29, ErrorCode30, ErrorCode38, ErrorCode39, ErrorCode40, ErrorCode45

from pandas.util.testing import assert_frame_equal
import unittest
import pandas
import numpy
import os


class TestGetFiles(unittest.TestCase):

    def test_GetFiles(self):
        print('\ntest_GetFiles:')
        print('        case 1: get the name of files from the user-defined directory')
        #input_dir = 'emmer/data/data_dir_2/'
        input_dir = 'emmer/data/data_dir_3/'
        multiple_input = GetFiles(input_dir = input_dir, suppress = False, second_chance = False)
        my_result = sorted(list(multiple_input.input_files))

        expected_result = [os.path.join(input_dir, 'group_A.csv'), os.path.join(input_dir, 'group_B.csv')]
        self.assertListEqual(my_result, expected_result)

        print('        ---------------------------------------------------')
        print('        case 2: test error handling (no csv in user-defined directory)')
        input_dir = 'emmer/data/data_dir_5/'
        with self.assertRaises(ErrorCode1):
            multiple_input = GetFiles(input_dir = input_dir, suppress = True, second_chance = False)
        print('===========================================================')


class TestRawDataImport(unittest.TestCase):

    def test_readCSV(self):
        print('\ntest_readCSV:')
        print('        case 1: read csv files')
        input_matrix = RawDataImport(file_name = 'emmer/data/test_case_1.csv', for_merging_file = False, suppress = False)
        input_matrix.readCSV()

        data = {'col1':[10, 21, 42, 21, 45 ,0],
                'col2':[1, 4, 10, 6, 14, 14],
                'col3':[2, 4, 2, 3, 1, 13],
                'col4':[0, 1, 0, 0, 0, 0],
                'col5':[12, 17, 18, 30, 14, 1],
                'col6':[50, 30, 26, 23, 25, 4]}
        expected_result = pandas.DataFrame(data, index =['sample1', 'sample2', 'sample3',
                                                       'sample4', 'sample5', 'sample7'])
        assert_frame_equal(input_matrix.data, expected_result)

        print('        ---------------------------------------------------')
        print('        case 2: test error handling')
        print('             2.1: file name should not contain "__"')
        with self.assertRaises(ErrorCode38):
            input_matrix = RawDataImport(file_name = 'emmer/data/data_dir_6/test__case_2.csv', for_merging_file = False, suppress = True)
            input_matrix.readCSV()

        print('        ---------------------------------------------------')
        print('             2.2: row name should not contain "__"')
        with self.assertRaises(ErrorCode39):
            input_matrix = RawDataImport(file_name = 'emmer/data/data_dir_6/test_case_1.csv', for_merging_file = False, suppress = True)
            input_matrix.readCSV()

        print('        ---------------------------------------------------')
        print('             2.3: input file name should ends with ".csv"')
        with self.assertRaises(ErrorCode1):
            input_matrix = RawDataImport(file_name = 'emmer/data/sow_test_dir_2/targert_file_1.txt', for_merging_file = False, suppress = True)
            input_matrix.readCSV()

        print('        ---------------------------------------------------')
        print('             2.4: file not found')
        with self.assertRaises(ErrorCode1):
            input_matrix = RawDataImport(file_name = 'emmer/data/data_dir_5/test.csv', for_merging_file = False, suppress = True)
            input_matrix.readCSV()
        print('===========================================================')


    def test_relativeAbundance(self):
        print('\ntest_RawDataImport.relativeAbundance:')
        input_matrix = RawDataImport(file_name = 'emmer/data/test_case_1.csv')
        input_matrix.readCSV()
        input_matrix.relativeAbundance()
        my_result = list(pandas.DataFrame.sum(input_matrix.data, axis = 1))
            # set axis = 1 to sum the rows

        expected_result = [1, 1, 1, 1, 1, 1]
        self.assertListEqual(my_result, expected_result)
        print('===========================================================')


    def test_detectionLimit(self):
        print('\ntest_RawDataImport.detectionLimit:')
        print('        case 1: complete entry that below the detection limit.\nThen remove empty row and column.')
        input_matrix = RawDataImport(file_name = 'emmer/data/test_case_1.csv', for_merging_file = False, suppress = True)
        input_matrix.readCSV()
        input_matrix.relativeAbundance()
        input_matrix.detectionLimit(detection_limit = 0.4)

        data = {'col1':[0, 0.428571, 0.454545 ,0],
                'col2':[0, 0, 0, 0.4375],
                'col3':[0, 0, 0, 0.40625],
                'col6':[0.666667, 0, 0, 0]}
        expected_result = pandas.DataFrame(data, index =['sample1', 'sample3', 'sample5', 'sample7'])
        assert_frame_equal(input_matrix.data, expected_result)
        print('===========================================================')


    def test_hardFilter(self):
        print('\ntest_RawDataImport.detectionLimit:')
        print('        case 1: complete entry that below the detection limit. Then remove empty row and column.')
        input_matrix = RawDataImport(file_name = 'emmer/data/test_case_1.csv', for_merging_file = False, suppress = True)
        input_matrix.readCSV()
        input_matrix.relativeAbundance()
        input_matrix.detectionLimit(detection_limit = 0.2)
        input_matrix.hardFilter(zero_tolerance_level = 0.5)
        my_result = list(input_matrix.feature_names)

        expected_result = ['col1', 'col6']
        self.assertListEqual(my_result, expected_result)
        print('===========================================================')


class TestMergeTargetedFiles(unittest.TestCase):

    def test_getMap(self):
        print('\ntest_MergeTargetedFiles.getMap:')
        print('        case 1: get mapping file')
        print('             1.1: correct mapping file')
        mapping_file = "emmer/data/sow_test_dir_2/correct_mapping_file.csv"
        target_file_dir = "emmer/data/sow_test_dir_2"
        suppress = False

        merge_target_files = MergeTargetedFiles(mapping_file = mapping_file, target_file_dir = target_file_dir,
                                                separate = '\t', suppress = suppress)
        merge_target_files.getMap()

        print(merge_target_files.map.columns.values)
        my_result = list(merge_target_files.map.columns.values)

        expected_result = ['file_name', 'sample_id', 'additional_note']
        self.assertListEqual(my_result, expected_result)

        print('        ---------------------------------------------------')
        print('             1.2: raise error when handling mapping file that has incorrect format')
        mapping_file = "emmer/data/sow_test_dir_2/incorrect_mapping_file.csv"
        target_file_dir = "emmer/data/sow_test_dir_2"
        suppress = True

        with self.assertRaises(ErrorCode40):
            merge_target_files = MergeTargetedFiles(mapping_file = mapping_file, target_file_dir = target_file_dir,
                                                    separate = '\t', suppress = suppress)
            merge_target_files.getMap()
        print('===========================================================')


        print('\ntest_MergeTargetedFiles.getTargetFile:')
        mapping_file = "emmer/data/sow_test_dir_2/correct_mapping_file.csv"
        target_file_dir = "emmer/data/sow_test_dir_2"
        target_file = "emmer/data/sow_test_dir_2/targert_file_1.txt"
        suppress = False

        merge_target_files = MergeTargetedFiles(mapping_file = mapping_file, target_file_dir = target_file_dir,
                                                separate = '\t', suppress = suppress)
        target = merge_target_files.getTargetFile(targeted_file = target_file, col_name = 'A')
        my_result = list(target.shape)

        expected_result = [3,2]
        self.assertListEqual(my_result, expected_result)
        print('===========================================================')


        print('\ntest_MergeTargetedFiles.mergeFile:')
        mapping_file = "emmer/data/sow_test_dir_2/correct_mapping_file.csv"
        target_file_dir = "emmer/data/sow_test_dir_2"
        suppress = False

        merged = MergeTargetedFiles(mapping_file = mapping_file, target_file_dir = target_file_dir,
                                                separate = '\t', suppress = suppress)
        merged.mergeFile()
        print(merged.merged_target_file)
        my_result = list(merged.merged_target_file.index)

        expected_result = ['feature_1', 'feature_2', 'feature_3', 'feature_4']
        self.assertListEqual(my_result, expected_result)
        print('===========================================================')


class TestRetrospectDataImport(unittest.TestCase):

    def test_RetrospectDataImport(self):
        print('\ntest_RetrospectDataImport:')
        print('        case 1: __init__ error handling')
        print('             1.1: input file contains null value')
        with self.assertRaises(ErrorCode45):
            imported_bake_data = RetrospectDataImport(file_name = 'emmer/data/problem_maker/read_module/information_rich_features_summary_w_NA.csv', type = 'reproducibility', dimension = 'n', suppress = True)


        print('        ---------------------------------------------------')
        print('             1.2: file not found')
        with self.assertRaises(ErrorCode1):
            imported_bake_data = RetrospectDataImport(file_name = 'emmer/data/problem_maker/read_module/a_file_that_never_exist.csv', type = 'coordinate', dimension = 'n', suppress = True)


        print('        ---------------------------------------------------')
        print('        case 2. "coordinate" error handling')
        print('             2.2: input only contains coordinate for one PC')
        with self.assertRaises(ErrorCode11):
            imported_bake_data = RetrospectDataImport(file_name = 'emmer/data/problem_maker/read_module/PC1_only_coordinates.csv', type = 'coordinate', dimension = 'n', suppress = True)


        print('        ---------------------------------------------------')
        print('        case 3. "reproducibility"')
        print('             3.1: expect to work')
        print('             3.1.1.: summarized reproducibilty output')
        print('                     row: information-rich taxa; column: group')
        imported_repro_data = RetrospectDataImport(file_name = 'emmer/data/bake_data_dir_8/case1.csv', type = 'reproducibility', suppress = False)
        my_result = numpy.mean(numpy.array(imported_repro_data.reproducibility))
        expected_result = 0.40625
        self.assertAlmostEqual(my_result, expected_result)


        print('             3.1.2.: reproducibilty output from a single input file')
        print('                     row: information-rich taxa; column: ["feature_name", "occurrence", "repreducibility (%)"]')
        imported_repro_data = RetrospectDataImport(file_name = 'emmer/data/bake_data_dir_8/case2.csv', type = 'reproducibility', suppress = False)
        my_result = numpy.mean(numpy.array(imported_repro_data.reproducibility))
        expected_result = 75.6302521008403
        self.assertAlmostEqual(my_result, expected_result)


        print('        ---------------------------------------------------')
        print('        case 4: unexpected input format when type == "data_color_shape_and_fill"')
        print('             4.1: incorrect column header')
        with self.assertRaises(ErrorCode29):
            imported_bake_data = RetrospectDataImport(file_name = 'emmer/data/problem_maker/read_module/incorrect_header_data_color_shape_and_fill.csv', type = 'data_color_shape_and_fill', dimension = 'n', suppress = True)

        print('        ---------------------------------------------------')
        print('             4.2: no column header named edge_color')
        with self.assertRaises(ErrorCode30):
            imported_bake_data = RetrospectDataImport(file_name = 'emmer/data/problem_maker/read_module/no_edge_color.csv', type = 'data_color_shape_and_fill', dimension = 'n', suppress = True)


        print('        ---------------------------------------------------')
        print('        case 5: unexpected input file for "precent_explained"')
        with self.assertRaises(ErrorCode9):
            imported_bake_data = RetrospectDataImport(file_name = 'emmer/data/problem_maker/read_module/incorrect_precent_explained.csv', type = 'precent_explained', dimension = 'n', suppress = True)



if __name__ == '__main__':
    unittest.main()
