#!/usr/bin/env python3

from ..warn.warning import *
from ..err.error import *

import matplotlib.colors as mcolors
from matplotlib import markers
import re


"""
Handle all the input messages in EMMER
"""
class TestInputLength:
    """
    Make sure that the number of element in input matches the number of cluster, group,
    or individuals.
    """
    def __init__(self, set, input, expect = 0):
        self.set = set
        self.input = input
        self.expect = expect

    def testLen(self):
        try:
            if len(self.set) != len(self.input):
                raise ErrorCode10(add_msg = [self.input, self.set], suppress = False, second_chance = True)
            else:
                self.dictionary = dict(zip(self.set, self.input))

        except ErrorCode10:
            new_input = input('Please re-enter your input:\n').split(';')  ## TODO: not protected

            try:
                if len(self.set) != len(new_input):
                     raise ErrorCode10(add_msg = [self.input, self.set], suppress = False, second_chance = False)
                else:
                     self.input = new_input
                     self.dictionary = dict(zip(self.set, self.input))  #zip(keys, values)
            except ErrorCode10:
                pass

    # TODO: check input type


class InputCode1:
    """
    Input edge or fill color:
    Please assign color to each group or individuals.
    Please use semicolon to separate the assignment for each group or individuals.

    Location:
        individual.py

    Attributes:
        color_dict -- Type: dictionary
                      key: group; item: color
    """

    def __init__(self, set, add_msg, suppress, second_chance):
        count = 0
        colors = input(f'\n[[Input code 1]] Input {add_msg[0]} color:\nPlease assign color to each {add_msg[1]}.\n Please use semicolon to separate the assignment for each {add_msg[1]}\nExample 1:\nred;blue\nExample 2:\n#ff0000;#0000ff\n').split(';')
        check = TestInputLength(set = set, input = colors)
        check.testLen()

        ## first entry
        for element in check.input:
            if element in mcolors.cnames.keys() or element == 'none':
                pass
            else:
                hex_color = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', element)
                # ref: https://stackoverflow.com/questions/30241375/python-how-to-check-if-string-is-a-hex-color-code

                try:
                    if not hex_color:
                        raise ErrorCode28(add_msg = add_msg, suppress = suppress, second_chance = second_chance)
                except ErrorCode28:

        ## second entry
                    colors = input(f'\n[[Input code 1]] Input {add_msg[0]} color:\nPlease assign color to each {add_msg[1]}.\n Please use semicolon to separate the assignment for each {add_msg[1]}\nExample 1:\nred;blue\nExample 2:\n#ff0000,#0000ff\n').split(';')
                    check = TestInputLength(set = set, input = colors)
                    check.testLen()
                    print(check.input)

                    for element in check.input:
                        if element in mcolors.cnames.keys() or element == 'none':
                            pass
                        else:
                            hex_color = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', element)
                            # ref: https://stackoverflow.com/questions/30241375/python-how-to-check-if-string-is-a-hex-color-code

                            try:
                                if not hex_color:
                                    raise ErrorCode28(add_msg = add_msg, suppress = suppress, second_chance = False)

                            except ErrorCode28:
                                pass

        ## pass all tests, save in attribute
        self.color_dict = check.dictionary


class InputCode2:
    """
    Input cluster assignment:
    Please assign cluster to each group.

    Location:
        permanova.py

    Attributes:
        color_dict -- Type: dictionary
                      key: group; item: color
    """

    def __init__(self, set, suppress, second_chance):
        count = 0
        cluster = input(f'\n[[Input code 2]] Input cluster assignment:\nPlease assign cluster to each group.\n').split(';')
        check = TestInputLength(set = set, input = cluster)
        check.testLen()

        ## first entry
        try:
            if len(check.dictionary) > 2:
                raise ErrorCode37(suppress = suppress, second_chance = True)

        ## second entry
        except ErrorCode37:
            cluster = input(f'\n[[Input code 2]] Input cluster assignment:\nPlease assign cluster to each group.\n').split(';')
            check = TestInputLength(set = set, input = cluster)
            check.testLen()

            try:
                if len(check.dictionary) < 2:
                    raise ErrorCode37(suppress = suppress, second_chance = False)
            except ErrorCode37:
                pass

        ## pass all tests, save in attribute
        print(check.dictionary)
        self.cluster_dict = check.dictionary


class InputCode3:
    """
    Multiple choices:
    Ask user to choice one from the list.

    Location:
        bake.py

    Attributes:
        choice --
    """

    def __init__(self, choice, add_msg, suppress, second_chance):
        option = input(f'[[Input code 3]] {add_msg}. Acceptable choice includes: {choice}\n')
        # add_msg = 'please choose retrospect mode'
        # choice = ['Individual', 'Permanova', 'Reproducibility', 'RevisitThreshold', 'Bifurication']

        ## first entry
        try:
            if option not in choice:
                raise ErrorCode9(add_msg = choice, suppress = False, second_chance = True)

        ## second entry
        except ErrorCode9:
            option = input(f'[[Input code 3]] {add_msg}. Acceptable choice includes: {choice}\n')

            try:
                if option not in choice:
                    raise ErrorCode9(add_msg = choice, suppress = False, second_chance = False)
            except ErrorCode9:
                pass

        self.select = option


class InputCode4:
    """
    Please assign shape to each group or individuals.
    Please semicolon comma to separate the assignment for each group or individuals.
    More shape information (https://matplotlib.org/api/markers_api.html).

    Location:
        individual.py

    Attributes:
        color_dict -- Type: dictionary
                      key: group; item: shape
    """

    def __init__(self, set, add_msg, suppress, second_chance):
        count = 0
        shape = input(f'[[Input code 4]] Please assign shape style to each {add_msg}.\nPlease use semicolon to separate the assignment for each {add_msg}.\nExample:\no;s\nMore shape information (https://matplotlib.org/api/markers_api.html).\n').split(';')
        check = TestInputLength(set = set, input = shape)
        check.testLen()

        ## first entry
        for element in check.input:
            try:
                if element not in markers.MarkerStyle.markers.keys():
                    raise ErrorCode33(add_msg = add_msg, suppress = suppress, second_chance = second_chance)

        ## second entry
            except ErrorCode33:
                shape = input(f'[[Input code 4]] Please assign shape style to each {add_msg}.\nPlease use semicolon to separate the assignment for each {add_msg}.\nExample:\no;s\nMore shape information (https://matplotlib.org/api/markers_api.html).\n').split(';')
                check = TestInputLength(set = set, input = shape)
                check.testLen()

                try:
                    for element in check.input:
                        if element in markers.MarkerStyle.markers.keys():
                            pass
                        else:
                            raise ErrorCode33(add_msg = add_msg, suppress = suppress, second_chance = False)
                except ErrorCode33:
                    pass

        ## pass all tests, save in attribute
        self.shape_dict = check.dictionary


class InputCode5:
    """
    Allow users to choose whether they want to color by group or by individuals

    Location:
        individual.py

    Attributes:
        decision -- Type: string
    """

    def __init__(self, add_msg, suppress, second_chance):
        decision = input(f'\n[[Input Code 5]] Please decide whether you want to set {add_msg} by group or individual.\nPlease enter one of following options ["Group", "Individaul"]\n')

        try:
            if decision in ["Group", "Individaul"]:
                self.decision = decision
            else:
                raise ErrorCode36(add_msg = add_msg, suppress = suppress, second_chance = second_chance)
        except ErrorCode36:
            decision = input(f'\n[[Input Code 5]] Please decide whether you want to set {add_msg} by group or individual.\nPlease enter one of following options ["Group", "Individaul"]\n')

            try:
                if decision in ["Group", "Individaul"]:
                    self.decision = decision
                else:
                    raise ErrorCode36(add_msg = add_msg, suppress = suppress, second_chance = False)
            except ErrorCode36:
                pass
