#!/usr/bin/python
import requests
from collections import defaultdict
import re
import json
# from ast import literal_eval
# import ahocorasick
import pickle
import os
from getngrams import run
import shutil


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


def complete_dictionary(text_list)
    with open('/Users/leigh/Desktop/words_dictionary.json') as words:
        words_dictionary = json.load(words)

    A = ahocorasick.Automaton()

    for index, word in enumerate(words_dictionary):
        A.add_word(word, (index, word))

    for item in text_list:
        print(item)
        print(list(A.keys(item)))
'''

def merge_csvs():
    allFiles = glob.glob(os.getcwd() + "/*.csv")
    with open('Dictionary.csv', 'wv') as outfile:
        for i, fname in enumerate(allFiles):
            with open(fname, 'rb') as infile:
                if i != 0:
                    infile.readline()
                shutil.copyfileobj(infile, outfile)


if __name__ == '__main__':
    # pathogen_path = "Put path here"
    base_words_path = "/Users/leighyeh/Desktop/pathogen_prevalence_code/MFD.txt"
    base_words = get_words(base_words_path)
    
    if len(base_words) > 10:
        j = 0
        while j < len(base_words):
            run(base_words[j:j + 10])
            j += 10

    else:
        run(base_words)
    # merge_csvs(output_path)
