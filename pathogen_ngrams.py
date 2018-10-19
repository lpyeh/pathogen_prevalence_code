#!/usr/bin/python
import requests
from collections import defaultdict
import re
import json
# from ast import literal_eval
import ahocorasick
import pickle
import os
from getngrams import run
import shutil
import itertools
import pandas as pd
import sys

# Returns list of words to use as target words 
def dictionary_text(url):
    MFD = []
    # This pattern includes the * on the end of the words that have it in the dictionary,
    # take it out of re.compile if we don't want it
    r = re.compile(r'([a-zA-Z]+)')
    f = requests.get(url)

    # TODO: Do we want the mapping from word to type?
    for line in f.iter_lines():
        line = line.translate(None, b'%\t').decode()
        MFD.append(line)

    # Get only the necessary lines
    MFD = MFD[14:]
    # Get rid of empty spots in list
    MFD = list(filter(None, MFD))

    # Clean up text, now have a list of words from MFD
    for line in range(1, len(MFD)):
        text = r.search(MFD[line])
        MFD[line] = text.group(0)
    return MFD


def get_words(path):
    word_list = open(path).read().splitlines()
    # print(word_list)
    return word_list
'''
# Returns list of words to use as base words (AKA pathogen prevalence words)
def pathogen_text(path):
    pathogen_list = []
    return pathogen_list

'''
def complete_dictionary(text_list):
    complete_list = []
    with open('words_dictionary.json') as words:
        words_dictionary = json.load(words)

    A = ahocorasick.Automaton()

    for index, word in enumerate(words_dictionary):
        A.add_word(word, (index, word))

    for item in text_list:
        complete_list.append(list(A.keys(item)))
    
    return list(itertools.chain.from_iterable(complete_list))


def ngrams(mfd_list):
    if len(mfd_list) > 10:
        j = 0
        while j < len(mfd_list):
            run(mfd_list[j:j + 10])
    else:
        run(mfd_list)
    print("Finished getting ngrams for the text list")


def merge_csvs(length):
    combined_csv = pd.concat([pd.read_csv(f, header=None) for f in os.listdir(os.getcwd()) if f.endswith('.csv')], ignore_index=True)
    # print(combined_csv)
    combined_csv.to_csv(length + "MFD-combined-csv.csv", index=False)

if __name__ == '__main__':
    
    arg_string = ' '.join(sys.argv[1:])
    params = [arg for arg in arg_string if arg.startswith('-')]
    if params is '':
        long_mfd = False
        short_mfd = True
    
    for param in params:
        if '-long' in param:
            long_mfd = True
        elif '-short' in param:
            short_mfd = True
        elif '-both' in param:
            long_mfd = True
            short_mfd = True
    


    # pathogen_path = "Put path here"
    mfd_url = \
            'https://www.moralfoundations.org/sites/default/files/files/downloads/moral%20foundations%20dictionary.dic'
    base_words_path = "/Users/leighyeh/Desktop/pathogen_prevalence_code/MFD.txt"
    base_words = get_words(base_words_path)
    full_mfd = dictionary_text(mfd_url)
    # print(full_mfd)
    expanded_mfd = complete_dictionary(full_mfd)

    if long_mfd:
        ngrams(expanded_mfd)
        merge_csvs("long")
    
    if short_mfd:
        ngrams(base_words)
        merge_csvs("short")
    
    # merge_csvs("merged")
