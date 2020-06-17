#!/usr/bin/env python3
#from support import printForUnittest
import sys
import io

__version__ = 'v0.8.c.4+'

"""
=========================================================================================
Handle all the warning messages in EMMER.

In EMMER, errors always need to be address to ensure the completely excution. Warnings, on
the other hand, are usually non-critical and can be automatically fixed by EMMER.
==========================================================================================
"""

#class Warning(Exception):  # TODO: to retire (maybe)
#    """
#    Warning class
#
#    Arguments:
#        code -- Type: str
#                error code number in str
#
#    Attributes:
#        code -- Type: str
#    """
#    def __init__(self, code):
#        self.code = code


def reportWarning(fn):
    """
    What should emmer behave when warning occurs?
    1. Whether to print the docstring for WarningCode __init__ function.
       It is much easier to write detail explanation for each error or
       warning in docstring than in print()
    """
    def wapper(*args, **kwargs):

        silence = fn(*args, **kwargs)
        if silence == False:
            print(fn.__doc__)

        return

    return wapper


class WarningCode1(Warning):

    @reportWarning
    def __init__(self, silence):
        """
        [[Warning code 1]]
        Noncritial parameter setting error:
        When setting filter as "MinDataLostFilter", you do not have to set -z.

        emmer.harvest will neglect the -z argument and keep running.
        """
        return(silence)


class WarningCode2(Warning):

    @reportWarning
    def __init__(self, silence):
        """
        [[Warning code 2]]
        Noncritial parameter setting error:
        When setting filter as "None", you do not have to set -z.

        emmer.harvest will neglect the -z argument and keep running.
        """
        return(silence)


class WarningCode3(Warning):

    @reportWarning
    def __init__(self, silence):
        """
        [[Warning code 3]]
        Noncritial parameter setting error:
        Currently emmer does not support -sanityCheck (-s) option when designate a specific
        csv file or when designate a directory that only store one csv file.

        emmer.harvest will reset sanityCheck to False and keep running.
        """
        return(silence)

## TODO:
#  WarningCode4 available ###############################################################################################
## TODO


class WarningCode5(Warning):

    @reportWarning
    def __init__(self, silence):
        """
        [[Warning code 5]]
        Noncritial parameter setting error:
        Currently emmer does not support -plot (-p) option when designate a specific
        csv file or when designate a directory that only store one csv file.

        emmer.harvest will reset -plot to False and keep running.
        """
        return(silence)


class WarningCode6(Warning):

    @reportWarning
    def __init__(self, silence):
        """
        [[Warning code 6]]
        'output' folder exist in your working directory. Excuting emmer.tests will
        generate additional files in 'output' folder. Please consider to move your
        existing output file to other directory. Or remove 'output' folder to avoid
        confusion in the feature.
        """
        return(silence)


class WarningCode7(Warning):

    @reportWarning
    def __init__(self, silence):
        """
        [[Warning code 7]]
        Noncritial parameter setting error:
        Missing args.b (-b) setting. Will set the number of bin for generating
        histogram as 20
        """


class WarningCode8(Warning):

    @reportWarning
    def __init__(self, silence):
        """
        [[Warning code 8]]
        We are deeply sorry that the current version of emmer does not allow users
        to change shapes of data points on the PCA plot.

        This limitation might be related to issue 11155
        (https://github.com/matplotlib/matplotlib/issues/11155)

        We will try to enable the functions that allow user to define shapes of
        data points once this issue is resolved.

        If you have better solution, please contact emmer deveplors
        """
        return(silence)


class WarningCode9(Warning):

    @reportWarning
    def __init__(self, silence):
        """
        [[Warning code 9]]
        Expect arguments for -m
        """
        return(silence)


class WarningCode10(Warning):

    @reportWarning
    def __init__(self, silence):
        """
        [[Warning code 10]]
        Noncritial parameter setting error:
        You do not need to set threshold for reporting information-rich feature
        (-t) when using Quick Look Mode (-q).

        emmer.harvest will neglect the -t setting and keep running.
        """
        return(silence)


class WarningCode11(Warning):

    @reportWarning
    def __init__(self, silence):
        """
        [[Warning code 11]]
        Number of information-rich feature should not exceed the minimum number
        between number of row and number of column.
        """
        return(silence)


class WarningCode12(Warning):

    @reportWarning
    def __init__(self, silence):
        """
        [[Warning code 12]]
        Number of information-rich feature should not exceed the minimum number
        between number of row and number of column. Remove feature with less
        reproducibility before reprot the final list of information-rich features.
        """
        return(silence)


class WarningCode13(Warning):

    @reportWarning
    def __init__(self, silence):
        """
        [[Warning code 13]]
        Redundant and maybe conflicting parameter setting:
        When choose -m as ['Permanova', 'Individual'] and provide provide -p,
        emmer.bake will use the corrodinates in -p (not -i).

        To avoid potentially conflicting information regrading the coordinates, emmer.bake
        will neglect -i setting and use the coordinates from -p.
        """
        return(silence)
