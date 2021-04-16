#!/usr/bin/env python3

## usage
# at a level above emmer/
# python3 -m emmer.test.test_math

from ..main.basic.math import NonDesityMatrix
from ..posthoc.visual.viewer import Projection
from ..troubleshoot.err.error import ErrorCode41

import numpy.testing
import unittest
import pandas
import numpy


class TestNonDesityMatrix(unittest.TestCase):

    def test_NonDesityMatrix(self):
        print('\ntest_NonDesityMatrix:')
        print('        case 1: dataset only have one row')
        A = numpy.array([[1, 4, 5, 12]])

        with self.assertRaises(ErrorCode41):
            MatrixA = NonDesityMatrix(data = A, normalize = False, suppress = True)

    def test_normEigvals(self):
        print('\ntest_NonDesityMatrix.normEigvals:')
        print('        case 1: use covariance matrix (= centered -> SVD)')
        print('        case 1.1: detect error generated when coding the arithmetic steps')
        A = numpy.array([[1, 4, 5, 12], [5, 8, 9, 0], [6, 7, 11, 19]])
        MatrixA = NonDesityMatrix(A, normalize = False)
        my_result = list(numpy.sort(numpy.round(MatrixA.normEigvals(), decimals = 8)))
        expected_result = [0.        , 0.1744152, 0.8255848]  # can also be validated in R; prcomp (scale = F)
        numpy.testing.assert_almost_equal(my_result, expected_result)

        print('        ---------------------------------------------------')
        print('        case 1.2: detect error generating when using alternative arithmetic procedure to\neigendecomposition of the covariance matrix of the input matrix')
        eigenval = numpy.sort(numpy.linalg.eigvals(pandas.DataFrame(A).cov()))  # largest at the right most
        eigenval = eigenval[1:4]
        eigenval[eigenval < 10**-8] = 0
        expected_result = list(numpy.sort(numpy.round(eigenval/sum(eigenval), decimals = 8)))
        numpy.testing.assert_almost_equal(my_result, expected_result)
        print('===========================================================')

        print('        case 2: use correlation matrix (= centered -> scale -> SVD)')
        print('        case 2.1: detect error generated when coding the arithmetic steps')
        A = numpy.array([[1, 4, 5, 12], [5, 8, 9, 0], [6, 7, 11, 19]])
        MatrixA = NonDesityMatrix(A, normalize = True)
        my_result = list(numpy.sort(numpy.round(MatrixA.normEigvals(), decimals = 8)))
        expected_result = [0.        , 0.29255695, 0.70744305]
        numpy.testing.assert_almost_equal(my_result, expected_result)

        print('        ---------------------------------------------------')
        print('        case 2.2: detect error generating when using alternative arithmetic procedure to\neigendecomposition of the correlation matrix of the input matrix')
        A = numpy.array([[1, 4, 5, 12], [5, 8, 9, 0], [6, 7, 11, 19]])
        matrixForSVD = numpy.corrcoef(numpy.transpose(A))
        eigenval = numpy.linalg.eigvalsh(matrixForSVD)
        eigenval = eigenval[1:4]
        eigenval[eigenval < 10**-8] = 0
        expected_result = list(numpy.sort(numpy.round(eigenval/sum(eigenval), decimals = 8))) # can also be validated in R; prcomp (scale = T)
        numpy.testing.assert_almost_equal(my_result, expected_result)

    def test_vNE(self):
        print('test_NonDesityMatrix.vNE:')
        print('        case 1: calculate the von Neuman entropy correctly')
        A = numpy.array([[1, 4, 5, 12], [5, 8, 9, 0], [6, 7, 11, 19]])
        MatrixA = NonDesityMatrix(A, normalize = False)
        my_result = numpy.round(MatrixA.vNE(), decimals = 8)

        expected_result = 0.66770591
        numpy.testing.assert_almost_equal(my_result, expected_result)
        print('===========================================================')


    def test_numZeroEig(self):
        # the ability to count the number of zero in the list of normalized eigenvalues.
        # (one from the list of normEigvals; one from ncol - nrow)
        print('test_NonDesityMatrix.numZeroEig:')
        print('        case 1: the ability to count the number of zero in the list of normalized eigenvalues.\n(one from the list of normEigvals; one from ncol - nrow)')
        A = numpy.array([[1, 4, 5, 12], [5, 8, 9, 0], [6, 7, 11, 19]])
        MatrixA = NonDesityMatrix(A, normalize = False)
        my_result = MatrixA.numZeroEig()
        self.assertEqual(my_result, 2)
        print('===========================================================')


if __name__ == '__main__':
    unittest.main()
