#/usr/bin/python
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
import csv
from collections import defaultdict


value_dictionary = {
        'HarmVirtue': '01',
        'HarmVice': '02', 
        'FairnessVirtue': '03',
        'FairnessVice': '04',
        'IngroupVirtue': '05',
        'IngroupVice': '06',
        'AuthorityVirtue': '07',
        'AuthorityVice': '08',
        'PurityVirtue': '09',
        'PurityVice': '10',
        'MoralityGeneral': '11'
        }


'''
Returns a list of words from the Moral Foundations Dictionary website
'''
def dictionary_text(url):
    MFD = []
    MFD_dict = defaultdict(int)

    # Gets text
    text_pattern = re.compile(r'([a-zA-Z]+)')
    # Gets number associated with word (value category)
    num_pattern = re.compile(r'([0-9][0-9])')
    f = requests.get(url)

    for line in f.iter_lines():
        line = line.translate(None, b'%\t').decode()
        MFD.append(line)

    # Get only the necessary lines
    MFD = MFD[14:]
    # Get rid of empty spots in list
    MFD = list(filter(None, MFD))

    for line in range(1, len(MFD)):
        value = num_pattern.search(MFD[line])
        text = text_pattern.search(MFD[line])
        # MFD dictionary with (word : value category)
        MFD_dict[text.group(0)] = value.group(0)
        MFD[line] = text.group(0)
    
    return MFD, MFD_dict


'''
Returns a list of words given in text file
Requires: Text file be formatted with one word on each line
'''
def get_words(path):
    word_list = open(path).read().splitlines()
    # print(word_list)
    return word_list


'''
Returns a list of expanded words from text_list by using a large English dictionary (if there are incomplete lemmas in the text_list)
'''
def complete_dictionary(text_list):
    complete_list = []
    with open('words_dictionary.json') as words:
        words_dictionary = json.load(words)
    
    # Use ahocorasick to make looking up words faster
    A = ahocorasick.Automaton()

    for index, word in enumerate(words_dictionary):
        A.add_word(word, (index, word))

    for item in text_list:
        complete_list.append(list(A.keys(item)))
    
    return list(itertools.chain.from_iterable(complete_list))


'''
ngrams uses run function from getngrams.py from github.com/econpy/google-ngrams
'''
def ngrams(mfd_list):
    if len(mfd_list) > 10:
        j = 0
        while j < len(mfd_list):
            run(mfd_list[j:j + 10])
            j += 10
    else:
        run(mfd_list)
    print("Finished getting ngrams for the text list")


'''
Since getngrams.py can only handle a certain number of queries at a time (about 10-15), 
merge_csvs merges all the CSV files in current directory into one master one
'''
def merge_csvs(length):
    if not os.path.isdir('CSVs'):
        os.mkdir('CSVs')

    master_list = []
    for each_file in os.listdir(os.getcwd()):
        if each_file.endswith('.csv') and not each_file.startswith(length):
            master_list.append(pd.read_csv(each_file, parse_dates=[0]))
            os.remove(each_file)

    combined_csv = pd.concat(master_list, axis=1)
    file_name = length + "-MFD-combined.csv"
    os.chdir('CSVs')
    # print(combined_csv)
    combined_csv.to_csv(file_name, index=False)
    add_value_averages(file_name)


def add_value_averages(file_name):
    pd.read_csv(file_name, names=column_names)
    print(


if __name__ == '__main__':
    arg_string = ' '.join(sys.argv[1:]).lower()
    
    short_mfd_dict = defaultdict(int)
    long_mfd = False
    short_mfd = False
    
    if arg_string == '-long':
        long_mfd = True
    elif arg_string == '-short':
        short_mfd = True
    elif arg_string == '-both':
        long_mfd = True
        short_mfd = True

    # pathogen_path = "Put path here"
    mfd_url = \
            'https://www.moralfoundations.org/sites/default/files/files/downloads/moral%20foundations%20dictionary.dic'
    mfd_path = "/Users/leigh/Desktop/pathogen_prevalence_code/MFD.txt"
    short_mfd = get_words(mfd_path)
    mfd_list, long_mfd_dict = dictionary_text(mfd_url)
    
    for word in short_mfd:
        if word in long_mfd_dict:
            short_mfd_dict[word] = long_mfd_dict[word]


    '''
    expanded_mfd = complete_dictionary(mfd_list)

    # write expanded_mfd to text file
    with open("long_mfd.txt", "w") as outfile:
        for word in expanded_mfd:
            outfile.write(word + '\n')

    if long_mfd:
        print("Getting ngrams for long MFD")
        ngrams(expanded_mfd)
        print("Merging all the CSVs")
        merge_csvs("long")
    
    if short_mfd:
        print("Getting ngrams for short MFD")
        ngrams(short_mfd)
        print("Merging all the CSVs")
        merge_csvs("short")
    
    # merge_csvs("merged")
    '''
