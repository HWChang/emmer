#!/usr/bin/env python3

from ..troubleshoot.err.error import Error, ErrorCode23
#from sklearn.linear_model import LinearRegression
from scipy import stats
import pandas
import numpy
import sys
import os
import io


"""
A tool box of functions that could be used in almost all of the scripts in emmer package.
"""

##==0==##
def flattern(list_of_list):  ## TODO: it works, but need test
    """
    Flattern list of list to list.

    Example:
    A = [[1, 2], [3, 4]]
    B = flattern(A)
    > B = [1, 2, 3, 4]
    """
    flattern_list = [item for sublist in list_of_list for item in sublist]
    return(flattern_list)


def emptyNumpyArray(nrow, ncol):
    """
    Create empty numpy array and fill it with NaN.
    """
    numpy_array = numpy.zeros([nrow, ncol])
    numpy_array[:] = numpy.nan
    return(numpy_array)


def toFloat(number_in_str, suppress = False):
    """
    Convert interger to float
    """
    try:
        num = float(number_in_str)
        return(num)
    except ValueError as e:
        raise ErrorCode23(suppress = suppress) from e


def floatRange(input_tuple):
    """
    Based on the input tuple, create a list of float that starts with input_tuple[1] and end with input_tuple[0] with
    the increment of input_tuple[2]

    Note: cannot use range because it only accept int
    """
    max = input_tuple[0]
    min = input_tuple[1]
    step = input_tuple[2]

    float_list = []

    if max == min:
        float_list = [min]

    while min < (max + step):
        float_list.append(min)
        min += step

    return(float_list)


def addElementsInList(list_1, list_2):
    """
    list_1 = [A, B, C]
    list_2 = [X, Y, Z]

    list_3 = addElementsInList(list_1, list_2)
    > list_3 = [A+X, B+Y, C+Z]
    """
    ## TODO: current function is valnerable to error cause be uneven list length
    result_list = []
    for i in range(0, len(list_1)):
        result_list.append(list_1[i] + list_2[i])
    return(result_list)


def dualAssignment(dataframe, sep):
    """
    if columns == 'A-B' and sep = '-'
        separated this column into two columns

        if column 'A' already exist, but not column 'B':
            column 'A' + column 'A-B'
            create column 'B'
    """
    cols_need_works = [col for col in dataframe.columns if sep in col]
    dataframe_need_work = dataframe[cols_need_works]
    cols_not_need_works = [col for col in dataframe.columns if sep not in col]
    dataframe_not_need_work = dataframe[cols_not_need_works]

    dict = {}
    for c_1 in range(dataframe_not_need_work.shape[1]):
        list_to_hash = dataframe_not_need_work.iloc[:, c_1]
        key = dataframe_not_need_work.columns[c_1]
        if key in dict.keys():
            list_1 = dict[key]
            dict[key] = addElementsInList(list_1, list_to_hash)
        else:
            dict[key] = list_to_hash

    for c_2 in range(dataframe_need_work.shape[1]):
        list_2 = list(dataframe_need_work.iloc[:, c_2])
        key_list = str(dataframe_need_work.columns[c_2]).split(sep)

        for k in range(len(key_list)):
            if key_list[k] in dict.keys():
                list_1 = dict[key_list[k]]
                dict[key_list[k]] = addElementsInList(list_1, list_2)
            else:
                dict[key_list[k]] = list_2

    return(dict)
