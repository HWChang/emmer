#!/usr/bin/env python3

# Usage:
# move to one level above emmer/
# python3 -m emmer.tests

import unittest
from .troubleshoot.warn.warning import WarningCode6
from .troubleshoot.inquire.input import InputCode7

"""
Initiate all tests
"""


if __name__ == '__main__':
    # try:
    #     if path exist
    #         raise WarningCode6(silence = False)
    # except:
    #     inputCodeX

    answer = InputCode7(suppress = False)

    testsuite = unittest.TestLoader().discover('.')
    unittest.TextTestRunner(verbosity=1).run(testsuite)
