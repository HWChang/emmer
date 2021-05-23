#!/usr/bin/env python3

# Usage:
# go one level above emmer/
# python3 -m emmer.test.test_viewer

from ..main.basic.math import NonDesityMatrix
from ..posthoc.visual.viewer import Projection

from pandas.util.testing import assert_frame_equal
import numpy.testing
import unittest
import pandas
import numpy


class TestProjection(unittest.TestCase):

    def test_Projection(self):
        print('\ntest_Projection:')
        print('        Case 1: colmean')
        A = [[.1, .4, .5, .12], [.05, .08, .09, .00], [.6, .7, .11, .19]]
        A_df = pandas.DataFrame(A, columns = ['col1', 'col2', 'col3', 'col4'], index = ['sample1', 'sample2', 'sample3'])
        MatrixA_for_transformation = Projection(merged_dataframe = A_df, normalize = False)

        colmean = list(numpy.round(numpy.array(MatrixA_for_transformation.colmean), decimals = 6))
        my_result = colmean
        #scaler = list(numpy.round(numpy.array(MatrixA_for_transformation.scaler), decimals = 6))
        #my_result = scaler

        expected_result = [0.25, 0.393333, 0.233333, 0.103333]
        self.assertListEqual(my_result, expected_result)


        print('===========================================================')
        print('        Case 2: V')
        nrow = len(A_df.index.values)
        S = numpy.tile(colmean, (nrow, 1))
        #S = numpy.tile(scaler, (nrow, 1))
        A_mean_norm = numpy.array(A_df) - S
        # A_mean_norm
        # row: sample; col: feature

        projection = numpy.matmul(A_mean_norm, numpy.array(MatrixA_for_transformation.V))
        # projection
        # row: feature; col: principal components

        my_result = pandas.DataFrame(numpy.round(-projection[:, 0:2], decimals = 5))
        expected_result = pandas.DataFrame([[-0.12439, 0.28011],
                                            [-0.35851, -0.20217],
                                            [ 0.48290, -0.07794]])  ## can also be validated in R; prcomp(A, scale = F)$x  # note: flip sign
        assert_frame_equal(my_result, expected_result)


        print('===========================================================')
        print('        Case 3: matrixS_adj')
        MatrixA_for_transformation.cleanSpec()
        my_result = MatrixA_for_transformation.S_adj
        expected_result = numpy.array([[0.6141608, 0, 0, 0],
        	                           [0, 0.3541278, 0, 0],
        	                           [0, 0, 5.777891e-17, 0]])  ## can also be validated in R; svd(scale(A, scale = F))
        numpy.testing.assert_almost_equal(my_result, expected_result, decimal = 5)


        print('===========================================================')
        print('        Case 4: matrixU')
        print('        Case 4.1: matrixU itself')
        my_result = list(MatrixA_for_transformation.U[:, 0])

        expected_result = [0.20254078, 0.58373539, -0.78627618]
        numpy.testing.assert_almost_equal(my_result, expected_result)


        print('===========================================================')
        print('        Case 5: spec_cleaned_data')
        print('        Case 5.1: a special matrix that has three singular values')
        print('                  In this special example, we got three non-zero singular values')
        print('                  (including the 10^-17 one), the result should equal to the')
        print('                  matrix before conducting SVD.')
        my_result = MatrixA_for_transformation.spec_cleaned_data

        expected_result = MatrixA_for_transformation.matrixForSVD
        numpy.testing.assert_almost_equal(my_result, expected_result)

        print('        ---------------------------------------------------')
        print('        Case 5.2: a matrix that has more than three three singular values')
        print('                  Expect to consider only the first three singular values')
        print('                  when generating spec_cleaned_data. But spec_cleaned_data')
        print('                  should still have the same dimension as input matrix.')
        print('        Case 5.2.1: sanity check: make sure matrix B has more than three singular values')
        B = [[.1, .4, .5, .12], [.05, .08, .09, .00], [.6, .7, .11, .19], [.7, .7, .5, .2], [.1, .05, .9, .6]]
        B_df = pandas.DataFrame(B, columns = ['col1', 'col2', 'col3', 'col4'], index = ['sample1', 'sample2', 'sample3', 'sample4', 'sample5'])
        MatrixB_for_transformation = Projection(merged_dataframe = B_df, normalize = False)
        my_result = numpy.size(MatrixB_for_transformation.S, 0)

        self.assertEqual(my_result > 3, True)

        print('        ---------------------------------------------------')
        print('        Case 5.2.2: only consider the three singular values')
        MatrixB_for_transformation.cleanSpec()
        my_result = len(MatrixB_for_transformation.S_adj[numpy.nonzero(MatrixB_for_transformation.S_adj)])

        expected_result = 3
        self.assertEqual(my_result, expected_result)

        print('        ---------------------------------------------------')
        print('        Case 5.2.3: number of columns in spec_cleaned_data')
        my_result = numpy.size(MatrixB_for_transformation.spec_cleaned_data, 1)

        expected_result = 4  # ncol in input matrix B
        self.assertEqual(my_result, expected_result)

        print('        ---------------------------------------------------')
        print('        Case 5.2.4: number of rows in spec_cleaned_data')
        my_result = numpy.size(MatrixB_for_transformation.spec_cleaned_data, 0)

        expected_result = 5  # nrow in input matrix B
        self.assertEqual(my_result, expected_result)


        print('===========================================================')
        print('        Case 6: when set normalize == True')
        C = [[.1, .4, .5, .12], [.05, .08, .09, .00], [.6, .7, .11, .1]]
        C_df = pandas.DataFrame(C, columns = ['col1', 'col2', 'col3', 'col4'], index = ['sample1', 'sample2', 'sample3'])
        MatrixC_for_transformation = Projection(merged_dataframe = C_df, normalize = True)
        my_result = numpy.array(MatrixC_for_transformation.projection_df)

        expected_result = numpy.array([[-0.3329589,-1.4108734, 3.816392e-16],
                                       [ 1.7064763, 0.4766556, 1.325329e-15],
                                       [-1.3735174, 0.9342178,-1.963707e-15]])  ## can also be validated in R; prcomp(A, scale = F)$x  # note: flip sign
        numpy.testing.assert_almost_equal(my_result, expected_result)


if __name__ == '__main__':
    unittest.main()
