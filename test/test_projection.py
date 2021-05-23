#!/usr/bin/env python3

## usage
# at a level above emmer/
# python3 -m emmer.test.test_projection

from ..bake import BakeCommonArgs
from ..main.basic.read import RawDataImport, RetrospectDataImport
from ..posthoc.visual.projection import ProjectionArgs, projectNew
from ..toolbox.technical import flattern, emptyNumpyArray
from ..troubleshoot.err.error import *

import numpy.testing as npt
import unittest
import pandas
import numpy
import os


class TestProjectionArgs(unittest.TestCase):

    def Test_ProjectionArgs(self):
        print('\ntest_ProjectionArgs:')
        print('        case 1: error handling')
        print('             1.1: missing args.i')
        sys.argv[1:] = ['-m', 'Projection', '-i', 'emmer/data/bake_data_dir_9/']
        current_wd = os.getcwd()
        processed_args = BakeCommonArgs(suppress = True, test = False, neglect = True, silence = False)
        processed_args.getHomeKeepingArgs()

        with self.assertRaises(ErrorCode32):
            projection_args = ProjectionArgs(args = processed_args.args, current_wd = current_wd,
                                             suppress = True)


        print('        ---------------------------------------------------')
        print('             1.2: unexpect v input')
        sys.argv[1:] = ['-m', 'Projection', '-i', 'emmer/data/bake_data_dir_9/filtered_infoRich__PCA_coordinates.csv',
                        '-v', 'emmer/data/bake_data_dir_9/']
        current_wd = os.getcwd()
        processed_args = BakeCommonArgs(suppress = True, test = False, neglect = True, silence = False)
        processed_args.getHomeKeepingArgs()

        with self.assertRaises(ErrorCode34):
            projection_args = ProjectionArgs(args = processed_args.args, current_wd = current_wd,
                                             suppress = True)


        print('        ---------------------------------------------------')
        print('             1.3: unexpect s1 or s2')
        print('             1.3.1: unexpect s1')
        sys.argv[1:] = ['-m', 'Projection', '-i', 'emmer/data/bake_data_dir_9/filtered_infoRich__PCA_coordinates.csv',
                        '-v', 'emmer/data/bake_data_dir_9/filtered_infoRich__transformation_matrix.csv',
                        '-s1', 'emmer/data/bake_data_dir_9/']
        current_wd = os.getcwd()
        processed_args = BakeCommonArgs(suppress = True, test = False, neglect = True, silence = False)
        processed_args.getHomeKeepingArgs()

        with self.assertRaises(ErrorCode35):
            projection_args = ProjectionArgs(args = processed_args.args, current_wd = current_wd,
                                             suppress = True)


        print('        ---------------------------------------------------')
        print('             1.3.2: unexpect s2')
        sys.argv[1:] = ['-m', 'Projection', '-i', 'emmer/data/bake_data_dir_9/filtered_infoRich__PCA_coordinates.csv',
                        '-v', 'emmer/data/bake_data_dir_9/filtered_infoRich__transformation_matrix.csv',
                        '-s1', 'emmer/data/bake_data_dir_9/filtered_infoRich__data_colmean.csv',
                        '-s2', 'emmer/data/bake_data_dir_9']
        current_wd = os.getcwd()
        processed_args = BakeCommonArgs(suppress = True, test = False, neglect = True, silence = False)
        processed_args.getHomeKeepingArgs()

        with self.assertRaises(ErrorCode16):
            projection_args = ProjectionArgs(args = processed_args.args, current_wd = current_wd,
                                             suppress = True)


        print('        ---------------------------------------------------')
        print('             1.4: mismatch v and s1')
        print('             1.4.1: do not have exactly the same feature names')
        sys.argv[1:] = ['-m', 'Projection', '-i', 'emmer/data/bake_data_dir_9/filtered_infoRich__PCA_coordinates.csv',
                        '-v', 'emmer/data/bake_data_dir_9/filtered_infoRich__transformation_matrix.csv',
                        '-s1', 'emmer/data/bake_data_dir_9/incorrect_colmean_1.csv']
        current_wd = os.getcwd()
        processed_args = BakeCommonArgs(suppress = True, test = False, neglect = True, silence = False)
        processed_args.getHomeKeepingArgs()

        with self.assertRaises(ErrorCode42):
            projection_args = ProjectionArgs(args = processed_args.args, current_wd = current_wd,
                                             suppress = True)


        print('        ---------------------------------------------------')
        print('             1.4.2: feature names in -v and -s1 are not in the same order')
        sys.argv[1:] = ['-m', 'Projection', '-i', 'emmer/data/bake_data_dir_9/filtered_infoRich__PCA_coordinates.csv',
                        '-v', 'emmer/data/bake_data_dir_9/filtered_infoRich__transformation_matrix.csv',
                        '-s1', 'emmer/data/bake_data_dir_9/incorrect_colmean_2.csv']
        current_wd = os.getcwd()
        processed_args = BakeCommonArgs(suppress = True, test = False, neglect = True, silence = False)
        processed_args.getHomeKeepingArgs()

        with self.assertRaises(ErrorCode42):
            projection_args = ProjectionArgs(args = processed_args.args, current_wd = current_wd,
                                             suppress = True)


        print('        ---------------------------------------------------')
        print('             1.5: mismatch s1 and s2')
        sys.argv[1:] = ['-m', 'Projection', '-i', 'emmer/data/bake_data_dir_9/filtered_infoRich__PCA_coordinates.csv',
                        '-v', 'emmer/data/bake_data_dir_9/filtered_infoRich__transformation_matrix.csv',
                        '-s1', 'emmer/data/bake_data_dir_9/filtered_infoRich__data_colmean.csv',
                        '-s2', 'emmer/data/bake_data_dir_9/incorrect__data_colstd.csv']
        current_wd = os.getcwd()
        processed_args = BakeCommonArgs(suppress = True, test = False, neglect = True, silence = False)
        processed_args.getHomeKeepingArgs()

        with self.assertRaises(ErrorCode48):
            projection_args = ProjectionArgs(args = processed_args.args, current_wd = current_wd,
                                             suppress = True)


        print('        ---------------------------------------------------')
        print('             1.6: missing x')
        sys.argv[1:] = ['-m', 'Projection', '-i', 'emmer/data/bake_data_dir_9/filtered_infoRich__PCA_coordinates.csv',
                        '-v', 'emmer/data/bake_data_dir_9/filtered_infoRich__transformation_matrix.csv',
                        '-s1', 'emmer/data/bake_data_dir_9/filtered_infoRich__data_colmean.csv']
        current_wd = os.getcwd()
        processed_args = BakeCommonArgs(suppress = True, test = False, neglect = True, silence = False)
        processed_args.getHomeKeepingArgs()

        with self.assertRaises(ErrorCode43):
            projection_args = ProjectionArgs(args = processed_args.args, current_wd = current_wd,
                                             suppress = True)


        print('        ---------------------------------------------------')
        print('        case 2: expect to work')
        print('             2.1: single file')
        print('             2.1.1: s1')
        sys.argv[1:] = ['-m', 'Projection', '-i', 'emmer/data/bake_data_dir_9/filtered_infoRich__PCA_coordinates.csv',
                        '-v', 'emmer/data/bake_data_dir_9/filtered_infoRich__transformation_matrix.csv',
                        '-s1', 'emmer/data/bake_data_dir_9/filtered_infoRich__data_colmean.csv',
                        '-x', 'emmer/data/bake_data_dir_9/new_observation.csv']
        current_wd = os.getcwd()
        processed_args = BakeCommonArgs(suppress = True, test = False, neglect = True, silence = False)
        processed_args.getHomeKeepingArgs()

        projection_args = ProjectionArgs(args = processed_args.args, current_wd = current_wd,
                                         suppress = True)

        my_result = len(projection_args.input)
        expected_result = 1
        #['emmer/data/bake_data_dir_9/new_observation.csv']

        self.assertEqual(my_result, expected_result)


        print('        ---------------------------------------------------')
        print('             2.1.2: s1 and s2')
        sys.argv[1:] = ['-m', 'Projection', '-i', 'emmer/data/bake_data_dir_9/filtered_infoRich__PCA_coordinates.csv',
                        '-v', 'emmer/data/bake_data_dir_9/filtered_infoRich__transformation_matrix.csv',
                        '-s1', 'emmer/data/bake_data_dir_9/filtered_infoRich__data_colmean.csv',
                        '-s2', 'emmer/data/bake_data_dir_9/filtered_infoRich__data_colstd.csv',
                        '-x', 'emmer/data/bake_data_dir_9/new_observation.csv']
        current_wd = os.getcwd()
        processed_args = BakeCommonArgs(suppress = True, test = False, neglect = True, silence = False)
        processed_args.getHomeKeepingArgs()

        projection_args = ProjectionArgs(args = processed_args.args, current_wd = current_wd,
                                         suppress = True)

        my_result = len(projection_args.input)
        expected_result = 1
        #['emmer/data/bake_data_dir_9/new_observation.csv']

        self.assertEqual(my_result, expected_result)


        print('        ---------------------------------------------------')
        print('             2.2: mulitple file')
        print('             2.2.1: get correct file names')
        sys.argv[1:] = ['-m', 'Projection', '-i', 'emmer/data/bake_data_dir_9/filtered_infoRich__PCA_coordinates.csv',
                        '-v', 'emmer/data/bake_data_dir_9/filtered_infoRich__transformation_matrix.csv',
                        '-s1', 'emmer/data/bake_data_dir_9/filtered_infoRich__data_colmean.csv',
                        '-x', 'emmer/data/bake_data_dir_9/multiple_input_file']
        current_wd = os.getcwd()
        processed_args = BakeCommonArgs(suppress = True, test = False, neglect = True, silence = False)
        processed_args.getHomeKeepingArgs()

        projection_args = ProjectionArgs(args = processed_args.args, current_wd = current_wd,
                                         suppress = True)

        my_result = len(projection_args.input)
        expected_result = 2
        #['emmer/data/bake_data_dir_9/multiple_input_file/new_obs_case1.csv', 'emmer/data/bake_data_dir_9/multiple_input_file/new_obs_case2.csv']

        self.assertEqual(my_result, expected_result)

        print('        ---------------------------------------------------')
        print('             2.2.2: files merged correctly')
        my_result = len(flattern(projection_args.new_obs_merged[['ASV_100']].values.tolist()))
        expected_result = 30
        self.assertEqual(my_result, expected_result)

        my_result = len(flattern(projection_args.new_obs_merged[['ASV_100']].dropna().values.tolist()))
        expected_result = 13
        self.assertEqual(my_result, expected_result)

        my_result = flattern(projection_args.new_obs_merged[['ASV_100']].values.tolist())[0:12]
        expected_result = [0.004942689, 0.0, 0.0, 0.0017586879999999998, 0.0, 0.0, 0.0, 0.001431038, 0.004954967, 0.003545886, 0.002470356, 0.004484954]
        self.assertEqual(my_result, expected_result)


        print('        ---------------------------------------------------')
        print('             2.2.3: reorder input observation before scaling')
        my_result = flattern(projection_args.new_obs_merged_ordered[['ASV_1']].values.tolist())
        expected_result = [0.194372006, 0.0, 0.003101108, 0.0, 0.046333545999999996, 0.106633061, 0.185715338, 0.013310921000000002, 0.009116045, 0.035008113,
                           0.054677207, 0.002199074, 0.10117152900000001, 0.08226267599999999, 0.013001998, 0.017784772, 0.038146321000000004, 0.04967214599999999,
                           0.062960378, 0.10306026800000001, 0.040645482999999996, 0.163720676, 0.240451627, 0.23205805100000002, 0.038100764, 0.029639332, 0.06947714,
                           0.036716487, 0.0, 0.047442625999999995]
        self.assertEqual(my_result, expected_result)

        # make sure that the dimensionality is correct
        my_result = list(projection_args.new_obs_merged_ordered.shape)
        expected_result = [len(list(projection_args.new_obs_merged.index.values)), len(list(projection_args.colmean_df.feature_names))]
        self.assertEqual(my_result, expected_result)

        # make sure they are at the save order
        my_result = list(projection_args.new_obs_merged_ordered.columns.values)
        expected_result = list(projection_args.colmean_df.feature_names)
        self.assertEqual(my_result, expected_result)
        print('===========================================================')


class TestProjectNew(unittest.TestCase):

    def test_projectNew(self):
        print('\ntest_projectNew:')
        print('        case 1: s1')
        print('             1.1: expect to work')
        sys.argv[1:] = ['-m', 'Projection', '-i', 'emmer/data/bake_data_dir_9/filtered_infoRich__PCA_coordinates.csv',
                        '-v', 'emmer/data/bake_data_dir_9/filtered_infoRich__transformation_matrix.csv',
                        '-s1', 'emmer/data/bake_data_dir_9/filtered_infoRich__data_colmean.csv',
                        '-x', 'emmer/data/bake_data_dir_9/new_observation.csv',
                        '-o', 'unittest', '-r']
        current_wd = os.getcwd()
        processed_args = BakeCommonArgs(suppress = True, test = False, neglect = True, silence = False)
        processed_args.getHomeKeepingArgs()

        projection_new = projectNew(args = processed_args.args, current_wd = current_wd, retrospect_dir = current_wd,
                                output_file_tag = processed_args.output_file_tag, suppress = False)

        print('             1.2: dimensionality')
        my_result = list(projection_new.shape)
        expected_result = [47,7]
        self.assertEqual(my_result, expected_result)


        print('        ---------------------------------------------------')
        print('             1.3: check projecting result')
        result_df = projection_new[projection_new.index.str.startswith('new_observation__')][['PC1', 'PC2', 'PC3']]
        my_result = numpy.array(flattern(result_df.values.tolist()))
        expected_df = projection_new[projection_new.index.str.startswith('group_B__')][['PC1', 'PC2', 'PC3']]
        expected_result = numpy.array(flattern(expected_df.values.tolist()))
        npt.assert_almost_equal(my_result, expected_result, decimal = 3)

        os.remove('unittest__retrospect_both_new_and_original_coordinates.csv')
        os.remove('unittest__retrospect_project_new.csv')


        print('===========================================================')
        ## FIXME: Unable to use emmer.bake projection module when set emmer.harvest == T

        print('        case 2: s1 and s2')
        print('             2.1: expect to work')
        sys.argv[1:] = ['-m', 'Projection', '-i', 'emmer/data/bake_data_dir_9/s1_s2/filtered_infoRich__PCA_coordinates.csv',
                        '-v', 'emmer/data/bake_data_dir_9/s1_s2/filtered_infoRich__transformation_matrix.csv',
                        '-s1', 'emmer/data/bake_data_dir_9/s1_s2/filtered_infoRich__data_colmean.csv',
                        '-s2', 'emmer/data/bake_data_dir_9/s1_s2/filtered_infoRich__data_colstd.csv',
                        '-x', 'emmer/data/bake_data_dir_9/s1_s2/new_observations/new_obs_filterd_data.csv',
                        '-o', 'unittest', '-r']
        current_wd = os.getcwd()
        processed_args = BakeCommonArgs(suppress = True, test = False, neglect = True, silence = False)
        processed_args.getHomeKeepingArgs()

        projection_new = projectNew(args = processed_args.args, current_wd = current_wd, retrospect_dir = current_wd,
                                    output_file_tag = processed_args.output_file_tag, suppress = False)

        result_df = projection_new[projection_new.index.str.startswith('new_obs_filterd_data__')][['PC1', 'PC2', 'PC3']]  ## TODO: Work here!!!!
        my_result = numpy.array(flattern(result_df.values.tolist()))
        expected_df = projection_new[projection_new.index.str.startswith('group_A__')][['PC1', 'PC2', 'PC3']]
        expected_result = numpy.array(flattern(expected_df.values.tolist()))
        #npt.assert_almost_equal(my_result, expected_result, decimal = 3)       ## FIXME

        os.remove('unittest__retrospect_both_new_and_original_coordinates.csv')
        os.remove('unittest__retrospect_project_new.csv')

if __name__ == '__main__':
    unittest.main()
