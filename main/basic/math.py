#!/usr/bin/env python3

from ...troubleshoot.err.error import Error, ErrorCode41, ErrorCode46

import pandas
import numpy
import math

"""
This module stores the mathematical tools for converting the input matrix into
a density matrix and calculate the von Neumann entropy.
"""

class NonDesityMatrix:
    """
    Transform a numeric non-density matrix and calculate the von Neumann entropy.

    Arguments:
        data -- Type: RawDataImport.data (pandas.DataFrame)
        epsilon -- Type: int
                   Define machine percision. When set at '8', it means that the
                   machine percision is 10^-8
        use_cor_matrix -- Type: boolean
                          When set as True, calculated the eigenvalue from the
                          correlation matrix

    Attribute:
        data -- Type: numpy.ndarray
                Non-density matrix
        epsilon -- Type: float
                   Machine percision
        nrow -- Type: int
                Number of samples
        ncol -- Type: int
                Number of features
        colmean -- Type: numpy.ndarray
                   A matrix that has one row and <self.ncol> columns, each element in
                   this matrix represents the mean of its corresponding column in
                   <self.data>
        colstd -- Type: numpy.ndarray
                  A matrix that has one row and <self.ncol> columns, each element in
                  this matrix represents the standard deviation of its corresponding
                  column in <self.data>
        matrixForSVD -- Type: numpy.ndarray
                        A matrix that is transform from <self.data> and ready for SVD.
                        The transformation is conducted so the <self.matrixForSVD> will
                        satistify the following relationship:
                        eigendecompsition of <self.data> will generate eignevalue lamda
                        SVD of <self.matrixForSVD> will generate signular_value
                        lamda = (signular_value)^2
        normEigvals -- Type: numpy.ndarray
                       Normalized eigenvalues. The sum of all eigenvalues equals to one.
        vNE -- Type: numpy.float64
               The von Neumann entropy of the input numeric non-density matrix
        numZeroEig -- Type: numpy.int64
                      The number of normalized eigenvalues that equals to zero or less
                      than <self.epsilon>
    """
    def __init__(self, data, normalize, epsilon = 8, suppress = False):
        self.data = numpy.array(data)
        self.epsilon = 10 ** (-epsilon)
        self.normalize = normalize   # when True: use correlation matrix instead of covariance matrix
        self.nrow = numpy.size(self.data, 0)
        self.ncol = numpy.size(self.data, 1)
        self.suppress = suppress

        try:
            if self.nrow < 2:
                raise Error(code = '41')
        except Error as e:
            raise ErrorCode41(suppress = self.suppress) from e


    def normEigvals(self):
        """
        Prepare normalized eigenvalues for the von Neumann entropy calculation

        The math behide this computational process is:
        (signular_val of M)^2 = eigvals of (M * M.transpose)
        """

        ##--1--## preparing matrix
        # mean center the matrix:
        # the element in each column minus the corresponding colmean
        try:
            self.colmean = numpy.mean(numpy.array(self.data), axis = 0)
        except TypeError as e:
            raise ErrorCode46(suppress = self.suppress)

        S = numpy.tile(self.colmean, (self.nrow, 1))
        meanCenteredData = self.data - S

        if self.normalize == False:
            # equivalence of calculating eignevalues of a covariance matrix
            self.matrixForSVD = meanCenteredData
        else:
            # equivalence of calculating eignevalues of a correlation matrix
            self.colstd = numpy.std(numpy.array(meanCenteredData), ddof = 1, axis = 0)
            self.matrixForSVD = numpy.matmul(meanCenteredData, numpy.diag(1/self.colstd))

        ##--2--## calculate singular values
        s = numpy.linalg.svd(self.matrixForSVD, compute_uv = False)
        eigvalsFromSVD = numpy.power(s, 2)
        eigvalsFromSVD[eigvalsFromSVD < self.epsilon] = 0

        ##--3--## eigenvalues normalization
        normEigvals = eigvalsFromSVD/sum(eigvalsFromSVD)
        normEigvals[normEigvals < self.epsilon] = 0
        self.normEigvals = normEigvals
        return(self.normEigvals)


    def vNE(self):
        """
        Calculate the von Neumann entropy
        """
        beta = self.normEigvals()
        beta = numpy.array([i for i in beta if i != 0])
        self.vNE = sum(-numpy.transpose(beta)*numpy.log2(beta))
        return(self.vNE)


    def numZeroEig(self):
        """
        Report the number of eigenvalues that equals to zero in the vector of normalized eigenvalues
        """
        self.numZeroEig = sum(self.normEigvals() == 0)

        # the number of reported singular values equals to the min(self.nrow, self.ncol)
        if (self.nrow < self.ncol and self.numZeroEig > 0):
             self.numZeroEig = self.numZeroEig + (self.ncol - self.nrow)

        return(self.numZeroEig)
