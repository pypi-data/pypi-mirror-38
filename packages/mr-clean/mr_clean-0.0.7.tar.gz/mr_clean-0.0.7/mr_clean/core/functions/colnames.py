# -*- coding: utf-8 -*-
import re
from mr_clean._utils.substrings.substr_main import substr_list

def smart_colnames(df, cutoff = .5):
    """ Replace spaces and dashes with underscores and make everything lowercase
    remove underscores before and after
    replace multiple underscores with just one
    Create dictionary of taken words, with counts cooresponding to occurence rate

    Use N-grams to do this faster and easier -- dictionary of string tuples? Maybe an ordered list instead?

    Loop:
        Find words/phrases common among large portion of columns (according to cutoff)
        For each word/phrase:
            Replace each word in phrase with a single letter
            Loop:
                If already in dictionary:
                    add another letter to the abbrev. based on the original word phrase
                    try again
                else:
                    break
            replace phrase with abbreviation for all instances.
            Remove words of phrase from dictionary
            add abbreviation to the dictionary
            add (phrase,abbreviation) to list
    """

    col_list = []
    # Removing whitespace and making everything lowercase
    for col_name in df.columns:
        col_name = re.sub('[^a-zA-Z0-9]',' ',col_name)
        col_name = col_name.strip().lower()
        col_name = re.sub('\s+','_',col_name)

        col_list.append(col_name)

    # Dictionary of words in the columns
    word_dict,max_len = col_words(col_list)
    # Max len is 1 greater than the length of largest string tuple that we'll test for
    word_list = list(word_dict.keys())




    return col_list


def col_words(col_list):
    """ Get the list of words in the columns
    Parameters:
    col_list - list of strings
        List of column names
    """
    col_dict = {}
    max_len = 1
    for col_name in col_list:
        words = col_name.split('_')
        max_len = max(len(words),max_len)
        for word in words:
            if word in col_dict.keys():
                col_dict[word]+=1
            else:
                col_dict[word]=1
    return (col_dict,max_len)

def abbrev(phrase,word_length = 1):
    """ Abbreviates a phrase
    Parameters:
    phrase - str
        Phrase to abbreviate
    word_length - int, default 1
        Length of each word after abbreviation

    Ex:
        word_word_2word
    word_length 1: ww2w
    word_length 2: wowo2wo
    """
    word_list = phrase.split('_')
    abbreviation = ''
    for word in word_list:
        recording = 0
        for character in word:
            if isnum(character):
                recording = 0
                abbreviation+=character
            elif recording < word_length:
                abbreviation+=character
                recording+=1
    return abbreviation

def isnum(character):
    return character in ['0','1,','2','3','4','5','6','7','8','9']
