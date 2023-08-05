# -*- coding: utf-8 -*-

# Utility function get longest common substrings from a list of substrings

import pandas as pd
from anytree import Node
from mr_clean._utils.substrings.suffix_tree import suffix_tree
from mr_clean._utils.substrings.substr_list import substr_unfiltered

def substr_list(str_list,length = -1,min_freq = 2,repeats = True):
    """ Gets a list of common substrings, ordered by length
    Parameters:
    str_list - list of strings
        List of strings to find the common substrings of
    length - int, default -1
        Lower limit for the length of the strings in the list. All strings with length
        equal to or less than the limit are returned. If set to -1, then all will be returned
    min_freq - int, default 2
        Minimum frequency of the substring necessary to include it in the list
    repeats - bool, default True
        Whether or not elements in the list that originate as substrings of other elements will
        remain in the list.

    WARNING:
    If set to false, runtime of this function could increase substantially. Checking for repeats is
    currently on the order of O(n^2*s) operation, where n is the amount of elements and s is the
    average length of the strings in the list.

    Ex:
        substr_list(['dasdf','dfwed','_as'])
        output = ['df','as','a','s','d','f','w','e','_']

    Ex:
        substr_list(['dasdf','dfwed','_as'],length = 2)
        output = ['df','as']
    Ex:
        substr_list(['dasdf','dfwed','_as'],repeats = False)
        output = ['df','as','w','e','d','_']

        substr_list(['wasd','wasd','awa'],repeats = False)
        output = ['wasd','wa']
        Since 'sd','d','as', and 'asd' all are only present as substrings of 'wasd', they
        are not included in the final results. However, 'wa' is present both in 'wasd' and
        in 'awa', outside of the string 'wasd', and thus is included.
    """

    str_list = pd.Series(str_list)

    # Documentation for tree structure https://pypi.org/project/anytree/

    # Method: Suffix Tree https://en.wikipedia.org/wiki/Generalized_suffix_tree

    # Description: https://en.wikipedia.org/wiki/Longest_common_substring_problem

    # TODO Lol the entire thing

    # Plan

    # Get suffix tree

    # Get list of common substrings

    # Filter by length if necessary

    # Filter by repeats if necessary


    return substr_list


def sort_by_length(str_list):
    pass

def filter_by_length(str_list):
    pass
