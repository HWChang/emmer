#!/usr/bin/env python3

from ..warn.warning import *
from ..err.error import *

import matplotlib.colors as mcolors
from matplotlib import markers
import sys
import re



"""
Handle all the input messages in EMMER
"""

## TODO: no second change after failing input evaluation
#        python3 -m emmer.bake
#        x


class EvaluateInput:
    """
    Evaluate input from users.

    Arguments:
        input -- Type: list
                 User input
        set -- Type: set
               Set of corresponding elements that require user-input arguments
        suppress -- Type: boolean
                    Exit program after raise error or not
        second_chance -- Type: boolean
                         Give user a second chance to change the input argument or not
        expect -- Type: list or 0
                  Expected input values in list

    Attributes:
        input -- Type: list
        set -- Type: list
        suppress -- Type: boolean
        expect -- Type: list or 0
        map_input -- Type: dictionary
                     key: elements in set; item: user input
        passed -- Type: boolean
                  True: pass the evaluation; False: does not pass the evaluation but
                  users still have a second change to input arguments
    """

    def __init__(self, input, set, suppress, expect = 0):
        self.input = input
        self.set = list(set)
        self.suppress = suppress
        self.expect = expect
        self.passed = False


        print('self.input')
        print(self.input)
        print('self.set')
        print(self.set)

        ## the number of elements in input are as expected
        try:
            if len(set) != len(input):
                raise Error(code = '10')
            else:
                self.map_input = dict(zip(set, input))
                self.passed = True
        except Error as e:
            raise ErrorCode10(suppress = suppress)


    def checkDeveloperError(self):
        try:
            if self.expect != 0:
                raise Error(code = '31')
        except Error as e:
            raise ErrorCode31(suppress = self.suppress) from e


    def evaluateColor(self):
        """
        InputCode1 specific evaluation
        """
        self.passed = False
        EvaluateInput.checkDeveloperError(self)

        for element in self.input:
            if element in mcolors.cnames.keys() or element == 'none':
                # allow element == 'none' will give user to plotting partial data
                # onto the PCA plot
                self.passed = True
            else:
                hex_color = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', element)
                # ref: https://stackoverflow.com/questions/30241375/python-how-to-check-if-string-is-a-hex-color-code

                try:
                    if not hex_color:
                        raise Error(code = '28')   ## FIXME: unable to arise this error
                    else:
                        self.passed = True
                except Error as e:
                    raise ErrorCode28(suppress = self.suppress) from e


    def evaluateStatCluster(self):
        """
        InputCode2 specific evaluation
        """
        self.passed = False
        EvaluateInput.checkDeveloperError(self)

        # expect to have more than two clusters when running statistical test
        try:
            if len(list(set(self.input))) < 2:
                raise Error(code = '37')
            else:
                self.passed = True
        except Error as e:
            raise ErrorCode37(suppress = self.suppress) from e


    def evaluateModeOption(self):
        """
        InputCode3 specific evaluation

        ErrorCode9 is related to WarningCode9. When WarningCode9 arised, user can
        try to advert the error by providing appropriate input via InputCode3. However,
        if user fail to provide expected input, ErrorCode9 will arise and terminate the
        program. No second chance for re-entering.
        """
        self.passed = False

        try:
            if self.expect == 0:
                raise Error(code = '7')
            elif len(set(self.input).intersection(list(self.expect.values()) + list(self.expect.keys()))) == 0:
                raise Error(code = '9')
            else:
                self.passed = True
        except Error as e:
            if e.code == '7':
                raise ErrorCode7(suppress = self.suppress) from e
            elif e.code == '9':
                raise ErrorCode9(suppress = self.suppress) from e


    def evaluateMarker(self):
        """
        InputCode4 specific evaluation
        """
        self.passed = False
        EvaluateInput.checkDeveloperError(self)

        try:
            for element in self.input:
                if element not in markers.MarkerStyle.markers.keys():
                    raise Error(code = '33')
                else:
                    self.passed = True
        except Error as e:
            raise ErrorCode33(suppress = self.suppress) from e


    def evaluateGroupOption(self):
        """
        InputCode5 specific evaluation
        """
        self.passed = False

        try:
            if self.expect == 0:
                raise Error(code = '7')
            elif len(set(self.input).intersection(list(self.expect.values()) + list(self.expect.keys()))) == 0:
                raise Error(code = '36')
            else:
                self.passed = True
        except Error as e:
            if e.code == '7':
                raise ErrorCode7(suppress = self.suppress) from e
            elif e.code == '36':
                raise ErrorCode36(suppress = self.suppress) from e

## TODO: unclear whether I am assign to edge or fill
class InputCode1:
    """
    Input edge or fill color:
    Please assign color to each group or individuals.
    Please use semicolon to separate the assignment for each group or individuals.

    Arguments:
        set -- Type: list
        suppress -- Type: boolean

    Attributes:
        color_dict -- Type: dictionary
                      key: group; item: color
    """

    def __init__(self, set, suppress):
        """
        [[Input code 1]]
        Input color information:
        Please assign color to each group or individuals.
        Please use semicolon to separate the assignment for each group or individuals.

        Example:
        Assuming you have two groups, group_A and group_B. You want to assign red and blue to
        group_A and group_B respectively. You can enter:
        red;blue
        #ff0000;#0000ff
        #FF0000;#0000FF
        """
        print(self.__init__.__doc__)

        ## take input
        option = input('\n        Please enter your input:\n').split(';')

        ## evaluate input
        confirmed_input = EvaluateInput(input = option, set = set, suppress = True)

        if confirmed_input.passed == False:
            option = input('\n        Please enter your input:\n').split(';')
            confirmed_input = EvaluateInput(input = option, set = set, suppress = False)

        confirmed_input.evaluateColor()
        if confirmed_input.passed == False:
            option = input('\n        Please renter your input:\n').split(';')
            confirmed_input = confirmed_input = EvaluateInput(input = option, set = set, suppress = False)

        ## export input
        self.color_dict = confirmed_input.map_input


class InputCode2:
    """
    Input cluster assignment for PERMANOVA test.

    Arguments:
        set -- Type: list
        choice_dict -- Type: dictionary
                       Key: option number; item: full name of the option
        suppress -- Type: boolean

    Attributes:
        cluster_dict -- Type: dictionary
                        key: group; item: cluster
    """

    def __init__(self, set, suppress):
        """
        [[Input code 2]]
        Input cluster assignment:
        Please assign cluster to each group for PERMANOVA test.
        """
        print(self.__init__.__doc__)

        ## take input
        option = input('\n        Please re-enter your input:\n').split(';')

        ## evaluate input
        confirmed_input = EvaluateInput(input = option, set = set, suppress = True)

        if confirmed_input.passed == False:
            option = input('\n        Please re-enter your input:').split(';')
            confirmed_input = EvaluateInput(input = option, set = set, suppress = False)

        confirmed_input.evaluateStatCluster()
        if confirmed_input.passed == False:
            option = input('\n        Please re-enter your input:').split(';')
            confirmed_input = confirmed_input = EvaluateInput(input = option, set = set, suppress = False)

        ## export input
        self.cluster_dict = confirmed_input.map_input


class InputCode3:
    """
    Choose emmer.bake mode.

    In the future, this input class can be generalized to all of the multiple choice
    input in emmer

    Arguments:
        set -- Type: list
        choice_dict -- Type: dictionary
                       Key: option number; item: full name of the option
        suppress -- Type: boolean

    Attributes:
        selection -- Type: str
                     The full name of the option chose by the user
    """

    def __init__(self, set, choice_dict, suppress):
        """
        [[Input code 3]]
        Please choose emmer.bake mode. You can choose from the following options:

        [1] Individual
        [2] Permanova
        [3] RevisitThreshold
        [4] Reproducibility
        [5] Bifurication
        [6] Projection

        After you make your choose, please type the full name of the mode (e.g.
        'Individual') or option number (e.g. '1'). Please note that emmer.bake
        are case sensitive. In another word, 'individual' will not be accepted
        as legitimate input.

        Additional explanation on those methods:
        1. Individual: plot individual samples onto the PCA plot. Allow better flexibility in
                       aesthetics setting
        2. Permanova: conduct PERMANOVA test on different groups in the PCA plot
        3. RevisitThreshold: revisit threshold settings (args.t, args.l, and args.u) used in
                             emmer.harvest
        4. Reproducibility: summarizing information-rich feature calling reproducibility into
                            basic statistics and histogram
        5. Bifurication: identify information-rich features that help to differentiate different
                         groups on the PCA space.
        6. Projection: project new observation onto an existing PCA space.

        Please make your choice:
        """
        print(self.__init__.__doc__)

        ## take input
        option = input('\n        Please re-enter your input:\n').split(';')

        ## evaluate input
        confirmed_input = EvaluateInput(input = option, set = ['mode'], expect = choice_dict, suppress = True)

        if confirmed_input.passed == False:
            option = input('\n        Please re-enter your input:\n').split(';')
            confirmed_input = EvaluateInput(input = option, set = ['mode'], expect = choice_dict, suppress = False)

        confirmed_input.evaluateModeOption()
        if confirmed_input.passed == False:
            option = input('\n        Please re-enter your input:\n').split(';')
            confirmed_input = EvaluateInput(input = option, set = ['mode'], expect = choice_dict, suppress = False)

        ## export input
        if option[0] in choice_dict.keys():
            self.selection = choice_dict[option[0]]
        else:
            self.selection = option[0]


class InputCode4:
    """
    Please assign shape to each group or individuals.

    Arguments:
        set -- Type: list
        choice_dict -- Type: dictionary
                       Key: option number; item: full name of the option
        suppress -- Type: boolean

    Attributes:
        shape_dict -- Type: dictionary
                      key: group; item: shape
    """

    def __init__(self, set, suppress):
        """
        [[Input code 4]]
        Please assign shape to each group or individuals.
        Please semicolon comma to separate the assignment for each group or individuals.
        More shape information (https://matplotlib.org/api/markers_api.html).
        """
        print(self.__init__.__doc__)

        ## take input
        option = input('\n        Please enter your input:\n').split(';')

        ## evaluate input
        confirmed_input = EvaluateInput(input = option, set = set, suppress = True)

        if confirmed_input.passed == False:
            option = input('\n        Please enter your input:\n').split(';')
            confirmed_input = EvaluateInput(input = option, set = set, suppress = False)

        confirmed_input.evaluateMarker()
        if confirmed_input.passed == False:
            option = input('\n        Please enter your input:\n').split(';')
            confirmed_input = confirmed_input = EvaluateInput(input = option, set = set, suppress = False)

        ## export input
        self.shape_dict = confirmed_input.map_input


class InputCode5:
    """
    Allow users to choose whether they want to color by group or by individuals

    Arguments:
        set -- Type: list
        choice_dict -- Type: dictionary
                       Key: option number; item: full name of the option
        suppress -- Type: boolean

    Attributes:
        decision -- Type: string
    """

    def __init__(self, suppress):
        """
        [[Input code 5]]
        Please choose whether you want to color by group or by individuals.
        You can choose from the following options:

        [1] Group
        [2] Individaul

        Please make your choice:
        """
        print(self.__init__.__doc__)

        ## take input
        option = input('\n        Please enter your input:\n').split(';')
        decision_dict = {'1': 'Group', '2': 'Individaul'}

        ## evaluate input
        confirmed_input = EvaluateInput(input = option, set = ['mode'], expect = decision_dict, suppress = True)

        if confirmed_input.passed == False:
            option = input('\n        Please enter your input:\n').split(';')
            confirmed_input = EvaluateInput(input = option, set = ['mode'], expect = decision_dict, suppress = False)

        confirmed_input.evaluateGroupOption()
        if confirmed_input.passed == False:
            option = input('\n        Please enter your input:\n').split(';')
            confirmed_input = EvaluateInput(input = option, set = ['mode'], expect = decision_dict, suppress = False)

        ## export input
        self.decision = option


class InputCode6:
    """
    Allow users to add notes to the emmer_notebook

    Arguments:
        suppress -- Type: boolean

    Attributes:
        input_string -- Type: string
    """

    def __init__(self, suppress):
        """
        [[Input code 6]]
        Please enter an additional note in the emmer_notebook. Hit Enter once
        you finish entering your note.

        Your entry:
        """
        print(self.__init__.__doc__)

        self.input_string = input()


class InputCode7:
    """
    Reminding users that running emmer.tests will remove existing output files.

    Arguments:
        suppress -- Type: boolean

    Attributes:
        input_string -- Type: string
    """

    def __init__(self, suppress):
        """
        [[Input code 7]]
        Please note that running emmer.tests will remove existing output files.
        Please remember to backup those output files if you still want to use
        them in the future.

        Please enter "yes" when you ready to proceed?
        """
        print(self.__init__.__doc__)

        answer = input()

        if answer != "yes":
            sys.exit()
