## usage
# at a level above emmer/
# python3 -m emmer.test.test_bifurication

from ..bake import BakeCommonArgs
from ..posthoc.stats.bifurication import BifuricationArgs, linearRegressionPVal, DifferentiatingFeatures
from ..posthoc.visual.viewer import Projection
from ..troubleshoot.err.error import ErrorCode12, ErrorCode21

import numpy.testing
import unittest
import pandas
import numpy
import sys
import os


class TestBifuricationArgs(unittest.TestCase):

    def test_BifuricationArgs(self):
        print('\ntest_BifuricationArgs.:')
        print('        case 1: error handling')
        print('             1.1: missing both args.p and args.i setting. raise error for missing args.p')
        sys.argv[1:] = ['-m', 'Bifurication']
        current_wd = os.getcwd()
        processed_args = BakeCommonArgs(suppress = True, test = False, neglect = True, silence = False)
        processed_args.getHomeKeepingArgs()

        with self.assertRaises(ErrorCode12):
            bifurication_args = BifuricationArgs(args = processed_args.args, current_wd = current_wd,
            	                                 suppress = True)

        print('        ---------------------------------------------------')
        print('             1.2: missing args.i setting')
        sys.argv[1:] = ['-m', 'Bifurication', '-p', 'emmer/data/bake_data_dir_4/information_rich_features_summary.csv']
        current_wd = os.getcwd()
        processed_args = BakeCommonArgs(suppress = True, test = False, neglect = True, silence = False)
        processed_args.getHomeKeepingArgs()

        with self.assertRaises(ErrorCode21):
            bifurication_args = BifuricationArgs(args = processed_args.args, current_wd = current_wd,
                                                 suppress = True)

        print('        ---------------------------------------------------')
        print('             1.3: args.1 only contains one csv file')
        sys.argv[1:] = ['-m', 'Bifurication', '-p', 'emmer/data/bake_data_dir_4/information_rich_features_summary.csv',
                        '-i', 'emmer/data/data_dir_1']
        current_wd = os.getcwd()
        processed_args = BakeCommonArgs(suppress = True, test = False, neglect = True, silence = False)
        processed_args.getHomeKeepingArgs()

        with self.assertRaises(ErrorCode21):
            bifurication_args = BifuricationArgs(args = processed_args.args, current_wd = current_wd,
                                                 suppress = True)

        print('        ---------------------------------------------------')
        print('        case 2: expect to work')
        print('             2.1: get correct list of information-rich features')
        sys.argv[1:] = ['-m', 'Bifurication', '-p', 'emmer/data/bake_data_dir_4/information_rich_features_summary.csv',
                        '-i', 'emmer/data/bake_data_dir_4/filtered_data']
        current_wd = os.getcwd()
        processed_args = BakeCommonArgs(suppress = True, test = False, neglect = True, silence = False)
        processed_args.getHomeKeepingArgs()

        bifurication_args = BifuricationArgs(args = processed_args.args, current_wd = current_wd,
                                             suppress = True)

        my_result = bifurication_args.list_of_info_rich
        expected_result = ['ASV_1', 'ASV_15', 'ASV_2', 'ASV_3', 'ASV_32', 'ASV_4', 'ASV_7']

        self.assertListEqual(my_result, expected_result)

        print('        ---------------------------------------------------')
        print('             2.2: get correct number of input files')
        my_result = len(bifurication_args.input_files)
        expected_result = 2

        self.assertEqual(my_result, expected_result)
        print('===========================================================')


class TestLinearRegressionPVal(unittest.TestCase):

    def test_linearRegressionPVal(self):
        print('\ntest_linearRegressionPVal:')
        A = [[1,15,2], [1,11,1], [1,13,1], [0,2,1], [0,1,2], [0,3,1]]
        A_df = pandas.DataFrame(A, columns=['y','x1','x2'], index=['A__s1','A__s2','A__s3','B__s4','B__s5','B__s6'])
        target = A_df['y']
        data = A_df[['x1','x2']]

        my_result = numpy.array(linearRegressionPVal(target = target, data = data, silence_intersect = False))
        expected_result = numpy.array([0.7805, 0.0046, 0.6640]).reshape(3, 1)
            # result generated in R use lm() function

        numpy.testing.assert_almost_equal(my_result, expected_result, decimal = 4)
        print('===========================================================')


class TestDifferentiatingFeatures(unittest.TestCase):

    def test_differentiatingFeatures(self):
        print('\ntest_differentiatingFeatures:')
        print('        Case 1: dataset has a differentiating feature')
        A = [[15,2], [11,1], [13,1], [2,1], [1,2], [3,1]]
        A_df = pandas.DataFrame(A, columns=['feature_1','feature_2'], index=['A__s1','A__s2','A__s3','B__s4','B__s5','B__s6'])

        Projection_class_object = Projection(merged_dataframe = A_df, normalize = False)
        Projection_class_object.cleanSpec()

        DifferentiatingFeatures_class_object = DifferentiatingFeatures(Projection_class_object)
        DifferentiatingFeatures_class_object.atGroup()

        my_result = DifferentiatingFeatures_class_object.differentiating_feature

        expected_result = ['feature_1']

        self.assertListEqual(my_result, expected_result)

        print('        ---------------------------------------------------')
        print('        Case 2: dataset do not have differentiating feature')
        C = [[1,2], [3,1], [2,1], [2,1], [1,2], [3,1]]
        C_df = pandas.DataFrame(C, columns=['x1','x2'], index=['A__s1','A__s2','A__s3','B__s4','B__s5','B__s6'])

        Projection_class_object = Projection(merged_dataframe = C_df, normalize = False)
        Projection_class_object.cleanSpec()

        DifferentiatingFeatures_class_object = DifferentiatingFeatures(Projection_class_object)
        DifferentiatingFeatures_class_object.atGroup()

        my_result = len(DifferentiatingFeatures_class_object.differentiating_feature)

        expected_result = 0
        self.assertEqual(my_result, expected_result)
        print('===========================================================')


if __name__ == '__main__':
    unittest.main()
