#!/usr/bin/env python3

import sys

"""
Handle all the error messages in emmer.

In emmer, errors always need to be address to ensure the completely excution. Warnings, on
the other hand, are usually non-critical and can be automatically fixed by emmer.
"""

class Error(Exception):
    """
    Error class

    Arguments:
        code -- Type: str
                error code number in str

    Attributes:
        code -- Type: str
    """
    def __init__(self, code):
        self.code = code


def aftermath(fn):
    """
    What should emmer behave when error occurs?
    1. Print the docstring for ErrorCode __init__ function.
       It is much easier to write detail explanation for each error or
       warning in docstring than in print()
    2. Whether exist the program
       Suppress sys.exit() when running unittest
    """
    def wapper(*args, **kwargs):

        suppress = fn(*args, **kwargs)
        print(fn.__doc__)

        if suppress == False:
            sys.exit()
        return

    return wapper


class ErrorCode1(Error):

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 1]]
        Parameter setting error:
        Expect a input directory that contains at least one csv file or a specific
        file name end with ".csv" file.

        Example:
            'emmer/data/data_dir_3'
            'emmer/data/data_dir_3/group_A.csv'
        """
        return(suppress)


class ErrorCode2(Error):

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 2]]
        Parameter setting error:
        Expect: 0 < args.z <= 1.
        When set -z as 0.25, a column with more than 1/4 of its elements that are zeros
        will be removed before nominating information-rich features.
        """
        return(suppress)


class ErrorCode3(Error):

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 3]]
        Parameter setting error:
        Please set args.z (-z) when using hard filter. Expect: 0 < args.z <= 1.
        When set -z as 0.25, a column with more than 1/4 of its elements that are zeros
        will be removed before nominating information-rich features.
        """
        return(suppress)


class ErrorCode4(Error):

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 4]]
        Parameter setting error:
        No feature was selected.
        The information-rich feature selecting thresholds (-u, -l, -t) are too stringent.
        Please consider to relax the thresholds before rerun emmer.harvest

        After successful run emmer.harvest, you can use the "RevisitThreshold" mode in
        emmer.bake to refine theshold selection
        """
        return(suppress)


class ErrorCode5(Error):

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 5]]
        Parameter setting error:
        Must set at least one of thresholds (-u: upper; -l: lower) for information-rich
        feature selection.
        """
        return(suppress)


class ErrorCode6(Error):

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 6]]
        Parameter setting error:
        Expect detection limit args.d (-d) to be less than the greatest number in your
        input matrix. Please check your detection limit setting and re-run the program.
        """
        return(suppress)


class ErrorCode7(Error):

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 7]]
        Developer error:
        Expect to pass 'expect' argument when using EvaluateInput to evaulate the
        input code.

        Please note that not all of EvaluateInput evaluation needs a 'expect' argument.
        """
        return(suppress)


class ErrorCode8(Error):

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 8]]
        Parameter setting error:
        Expect a emmer.harvest-gereated csv file.

        The file usually stored under "output" folder with the keyword "projection"
        in its file name.
        """
        return(suppress)


class ErrorCode9(Error):

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 9]]
        Parameter setting error:
        Expect a emmer.harvest-gereated csv file that contain percent explain information
        for each PC.
        """
        return(suppress)


class ErrorCode10(Error):

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 10]]
        Unexpected user response error
        The number of the elements in the input, which should be separated by semicolon when
        user enter the input, does not match the number of attributes that needs input.

        For example, this error will arise when emmer.bake ask the user to define color for
        two groups of data on the PCA plot, but the number of color inputed by the user are
        not equal to two.
        """
        return(suppress)


class ErrorCode11(Error):

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 11]]
        Unexpected input error:
        Expect input PCA coordinate file to contain the coordinates for at least
        two dimensions.

        If you are using a emmer.harvest output file, please consider to relax
        your information-rich feature choosing thresholds. You can also run
        'RevisitThreshold' mode in emmer.bake to select a better threshold settings.
        """
        return(suppress)


class ErrorCode12(Error):

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 12]]
        Parameter setting error:
        Expect a csv file for args.p (-p)
        You can find the file for -p in output/*information_rich_features_summary.csv
        after running 'Bifurication' mode in emmer.bake
        """
        return(suppress)


class ErrorCode13(Error):

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 13]]
        Parameter setting error:
        Expect a directory that store all the *detail_vNE.csv generated from
        emmer.harvest

        Those files can are stored under "~/output/detial_vNE"
        """
        return(suppress)


class ErrorCode14(Error):

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 14]]
        Parameter setting error:
        Expect a directory that store all the *pre_filterd_data.csv generated from
        emmer.harvest

        Those files can are stored under "~/output/pre_filterd_data"
        """
        return(suppress)


class ErrorCode15(Error):

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 15]]
        Parameter setting error:
        direction designated by args.i (-i) should contain all and only the files
        that were used to generate the files in args.v (-v).
        """
        return(suppress)


class ErrorCode16(Error):

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 16]]
        Parameter setting error:
        Expect a single csv file that contains information for scaling the data matrix for calculating the
        PCA coordinate. This file is generated by emmer.harvest when set -n as True.

        Hint: the file stored under output/ that contains '__data_colstd' in file name.
        """
        return(suppress)


class ErrorCode17(Error):

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 17]]
        Parameter setting error:
        Expected to have three elements that are separated by comma from input argument.

        Example:
            -t '2,1,1'
            -u '3,2,1'
            -l '2,2,0'
        """
        return(suppress)


class ErrorCode18(Error):

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 18]]
        Parameter setting error:
        Expected to have at least one of these three setting (-t, -u, -l) when set -m
        as "RevisitThreshold"
        """
        return(suppress)


class ErrorCode19(Error):

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 19]]
        Parameter setting error:
        The first two elements in input should be a positive number that is greater than 0.

        These two numbers represent x-fold of standard deviation from the mean of the von
        Neumann entropy calculated from systemically remove one column (feature) at a time.
        Expect x > 0.
        """
        return(suppress)


class ErrorCode20(Error):

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 20]]
        Parameter setting error:
        The first two elements in input should be a positive number that is greater
        than 0.

        The numbers represent x-fold of standard deviation from the mean of the
        von Neumann entropy calculated from systemically remove one column (feature)
        at a time. Expect x > 0.
        """
        return(suppress)


class ErrorCode21(Error):

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 21]]
        Parameter setting error:
        Input directory (-i) should contains at least two .csv file. Please make
        sure you enter the correct directory path.

        Please refer to '/data/data_dir_3' as an example for the input dictory.
        """
        return(suppress)


class ErrorCode22(Error):

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 22]]
        Parameter setting error:
        The thrid element in arguments -u, -l, and -t represents the increment.
        Elements are separated by comma. Example: -u <max>,<min>,<increment>
        Expect the residual = 0 when divide the (max - min)/increment

        Please note the increment of -t setting can only be an interger.

        Example:
            -u 2,1,1
            -u 2,1,0.5
        """
        return(suppress)


class ErrorCode23(Error):

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 23]]
        Parameter setting error:
        Expect input as a an interger or a float.
        """
        return(suppress)


class ErrorCode24(Error):

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 24]]
        Parameter setting error:
        The thrid element in arguments -u, -l, and -t represents the increment.
        Base on your setting of the first and the second elements in this argument,
        EMMER except a number that is greater than zero.

        Example:
            -u '3,1,1'

        For the example above, emmer.bake will test three different -u setting:
        1, 2, and 3
        """
        return(suppress)


class ErrorCode25(Error):

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 25]]
        Parameter setting error:
        The thrid element in arguments -u, -l, and -t represents the increment.
        Base on your setting of the first and the second elements in this argument,
        EMMER except a number that is less than the first elements.

        Example:
            -u '3,1,1'
            -l '3,1,0.5'
        """
        return(suppress)


class ErrorCode26(Error):

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 26]]
        Parameter setting error:
        The thrid element in arguments -u, -l, and -t represents the increment.
        Base on your setting of the first and the second elements in this argument,
        EMMER except a number that equals to zero.

        Example:
            -u 2,2,0
        """
        return(suppress)


class ErrorCode27(Error):

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 27]]
        Parameter setting error:
        No information-rich feature was selected in any combination of the input
        threshold settings (-u, -l, -t)

        Suggestion:
            Select least stringent thresholds that include the original setting
            when user first run emmer.harvest
        """
        return(suppress)


class ErrorCode28(Error):

    @aftermath
    def __init__(self, suppress):
        """
        Unexpected user response:
        Expect matplotlib.colors (https://matplotlib.org/api/colors_api.html; for example: red,
        blue) or HEX color (#000000)

        Example:
        Assuming you have two groups, group_A and group_B. You want to assign red and blue to
        group_A and group_B respectively. You can enter:
        red;blue
        #ff0000;#0000ff
        #FF0000;#0000FF
        """
        return(suppress)


class ErrorCode29(Error):

    @aftermath
    def __init__(self, suppress = False):
        """
        Input file format error:
        Expect a csv file that has ['PC1', 'PC2'] or ['PC1', 'PC2', 'PC3'] as column names
        in the first two or three columns.

        The order of column names matters. A file that has the column name in ['PC2', 'PC1']
        order will also trigger this error code
        """
        return(suppress)


class ErrorCode30(Error):

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 30]]
        Parameter setting error:
        Expect a csv file to have ['group', 'individual', 'edge_color', 'fill_color', 'shape'] as
        column names.

        If you are not sure how to prepare -p file, you don't have use -p argument when running
        emmer.bake. The program will guild you through the process and prepare a -p file for your
        future analysis.

        Example:
            python3 -m emmer.bake -m 'Individual' -i <filtered_infoRich__PCA_coordinates.csv>
            python3 -m emmer.bake -m 'Permanova' -i <filtered_infoRich__PCA_coordinates.csv>
            python3 -m emmer.bake -m 'Reproducibility' -b 20 -i <information_rich_features_summary.csv>
            python3 -m emmer.bake -m 'RevisitThreshold' -u <2.5,1.5,0.25> -l <2.5,1.5,0.25> -v <output/detail_vNE/> -i <output/filtered_data/>
            python3 -m emmer.bake -m 'Bifurication' -i <filtered_data/> -p <information_rich_features_summary.csv>


        Group:
            Expect a csv file that has ['group'] as column names. In emmer.bake, the row of the
            input matrix represent each individual in each original input file for emmer. 'Group'
            are the same as orginal input file names.

        Individaul
            Expect a csv file that has ['individual'] as column names. In Retrospect, the row of the
            input matrix represent each individual in each original input file for emmer. 'individual'
            are the same as rows in orginal input files.

        edge_color:
            Expect a csv file that has ['edge_color'] as column names.

        fill_color:
            Expect a csv file that has ['fill_color'] as column names.

        Shape:
            Expect a csv file that has ['shape'] as column names.
        """
        return(suppress)


class ErrorCode31(Error):

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 31]]
        Developer error:
        Do not expect to pass 'expect' argument when using EvaluateInput to evaluateColor
        the input code.

        Please use the default expect setting. Let EvaluateInput.expect = 0
        """
        return(suppress)


class ErrorCode32(Error):

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 32]]
        Parameter setting error:
        Expect a single csv file that contains PCA coordinate generated by emmer.harvest

        Hint: the file stored under output/ that contains 'PCA_coordinates' in file name.
        """
        return(suppress)


class ErrorCode33(Error): #

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 33]]
        Parameter setting error:
        Expect matplotlib marker name (https://matplotlib.org/api/markers_api.html)
        """
        return(suppress)


class ErrorCode34(Error):

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 34]]
        Parameter setting error:
        Expect a single csv file that contains transformation matrix for generating the PCA coordinate.
        This file is generated by emmer.harvest

        Hint: the file stored under output/ that contains 'transformation_matrix' in file name.
        """
        return(suppress)


class ErrorCode35(Error):

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 35]]
        Parameter setting error:
        Expect a single csv file that contains information for scaling the data matrix for calculating the
        PCA coordinate. This file is generated by emmer.harvest

        Hint: the file stored under output/ that contains '__data_colmean' in file name.
        """
        return(suppress)


class ErrorCode36(Error):

    @aftermath
    def __init__(self, suppress):
        """
        Unexpected user response:
        Please choose between 'Group' or 'Individaul'
        ['Group', 'Individual']

        or use one the corresponding option number
        ['1', '2']
        """
        return(suppress)


class ErrorCode37(Error):

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 37]]
        Unexpected user response:
        Expect to have more than one cluster when running 'Permanova' mode
        """
        return(suppress)


class ErrorCode38(Error):

    @aftermath
    def __init__(self, suppress):
        """
        Input file naming error:
        Please avoid having "__" in the input csv file name.
        Having "__" will interfere with emmer.harvest and emmer.bake data handling

        Please refer to /data/data_dir_3 as an example for the input file format.
        """
        return(suppress)


class ErrorCode39(Error):

    @aftermath
    def __init__(self, suppress = False):
        """
        [[Error code 39]]
        Input file format error:
        Please avoid having "__" in row names of the input csv file.
        Having "__" will interfere with EMMER data handling

        Please refer to /data/data_dir_3/group_A.csv as example for
        emmer.harvest input file
        """
        return(suppress)


class ErrorCode40(Error):

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 40]]
        Input file format error:
        Expect column headers of the input mapping file to be "file_name"
        for the first column and "sample_id" for the second column.

        Please refer to /data/sow_test_dir_2/correct_mapping_file.csv as
        an example for the input mapping file.
        """
        return(suppress)



class ErrorCode41(Error):

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 41]]
        Expect input matrix (from args.i; -i) to have more than one row (sample).
        """
        return(suppress)


class ErrorCode42(Error):

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 42]]
        Parameter setting error:
        Input 'transformation_matrix' and '__data_colmean' might be from different analyses. Please
        choose the 'transformation_matrix' file and '__data_colmean' file generated from the same
        emmer.harvest run

        To pass:
        Make sure both file have exactly the same set of feature names (as rowname in
        'transformation_matrix'; as colname in '__data_colmean') and they are at the same order
        """
        return(suppress)


class ErrorCode43(Error):

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 43]]
        Parameter setting error:
        Expect new observation (args.x; -x)
        Expect a input directory that contains at least one csv file or a specific
        file name end with ".csv" file.

        Example:
            'emmer/data/data_dir_3'
            'emmer/data/data_dir_3/group_A.csv'
        """
        return(suppress)


class ErrorCode44(Error):  # TODO need unittest

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 44]]
        Log file already exist; raise error and stop emmer to avoid accidently remove
        previous log file without knowing.

        To prevent this error when running multiple emmer analyses in parallele, please
        provide a unique user-defined tag for each analysis via -o (args.o).
        """
        return(suppress)


class ErrorCode45(Error):

    @aftermath
    def __init__(self, suppress = False):
        """
        [[Error code 45]]
        Input file should not contains null value.
        """
        return(suppress)


class ErrorCode46(Error):       # TODO: unittest

    @aftermath
    def __init__(self, suppress = False):
        """
        [[Error code 46]]
        Expect a numeric input matrix. At least one of your column contains non-numeric
        values. Please check your input file(s).
        """
        return(suppress)


class ErrorCode47(Error):

    @aftermath
    def __init__(self, suppress = False):
        """
        [[Error code 47]]
        Parameter setting error:
        Number of CPU dedicated in this analysis should not exceed the number of
        CPU in your computer.
        """
        return(suppress)


class ErrorCode48(Error):

    @aftermath
    def __init__(self, suppress):
        """
        [[Error code 48]]
        Parameter setting error:
        Input '__data_colstd' and '__data_colmean' might be from different analyses. Please
        choose the '__data_colstd' file and '__data_colmean' file generated from the same
        emmer.harvest run.

        To pass:
        Make sure both file have exactly the same set of feature names and they are at the
        same order.
        """
        return(suppress)
