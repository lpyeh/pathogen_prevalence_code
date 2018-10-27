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


long_value_dictionary = {
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

short_value_dictionary = {
    'Care/HarmVirtue': ['kindness', 'compassion', 'nurture', 'empathy'],
    'Care/HarmVice': ['suffer', 'cruel', 'harm', 'hurt'],
    'Fairness/CheatingVirture': ['loyal', 'solidarity', 'patriot', 'fidelity'],
    'Fairness/CheatingVice': ['cheat', 'fraud', 'unfair', 'injustice'],
    'Loyalty/BetrayalVirtue': ['loyal', 'solidarity', 'patriot', 'fidelity'],
    'LoyaltyBetrayalVice': ['betray', 'treason', 'disloyal', 'traitor'],
    'AuthoritySubversionVirtue': ['authority', 'obey', 'respect', 'tradition'],
    'AuthoritySubversionVice': ['subversion', 'disobey', 'disrespect', 'chaos'],
    'PurityDegradationVirtue': ['purity', 'sacred', 'wholesome'],
    'PurityDegradationVice': ['impurity', 'depravity', 'degradation', 'unnatural']
}


'''
Returns a list of words from the Moral Foundations Dictionary website
'''
def dictionary_text(url):
    MFD = []
    MFD_dict = defaultdict(list)
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

    inv_value_dict = {v: k for k, v in long_value_dictionary.items()}

    for line in range(1, len(MFD)):
        value = num_pattern.search(MFD[line])
        text = text_pattern.search(MFD[line])
        if value.group(0) in inv_value_dict:
            MFD_dict[inv_value_dict[value.group(0)]].append(text.group(0))
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
    combined_csv.to_csv(file_name, index=False)


'''
Add averages for each moral foundation based on the dictionary (long or short)
'''
def add_value_averages(length, mapped_dict, mfd):
    if 'CSVs' in os.listdir(os.getcwd()):
        os.chdir('CSVs')

    for file in os.listdir(os.getcwd()):
        if file.startswith(length):
            csv = pd.read_csv(file)

    for key, value in mapped_dict.items():
        word_list = []
        for word in value:
            if word in mfd:
                word.strip()
                all_word = word + " (All)"
                if all_word in csv.columns.values:
                    word_list.append(all_word)
                elif word in csv.columns.values:
                    word_list.append(word)
        if word_list:
            csv[key] = csv[word_list].mean(axis=1)
            print(key)
            print(csv[key])

    file_name = length + "-MFD-with-averages.csv"
    csv.to_csv(file_name, index=False)


if __name__ == '__main__':
    # add_value_averages()

    arg_string = ' '.join(sys.argv[1:]).lower()
    
    short_mfd_dict = defaultdict(list)
    long = False
    short = True
    
    if arg_string == '-long':
        long = True
        short = False
    elif arg_string == '-both':
        long = True

    # pathogen_path = "Put path here"
    mfd_url = \
            'https://www.moralfoundations.org/sites/default/files/files/downloads/moral%20foundations%20dictionary.dic'
    mfd_path = "/Users/leigh/Desktop/pathogen_prevalence_code/MFD.txt"
    short_mfd = get_words(mfd_path)
    long_mfd, long_value_dict = dictionary_text(mfd_url)

    expanded_mfd = complete_dictionary(long_mfd)

    # write expanded_mfd to text file
    with open("long_mfd.txt", "w") as outfile:
        for word in expanded_mfd:
            outfile.write(word + '\n')

    if short:
        print("Getting ngrams for short MFD")
        ngrams(short_mfd)
        print("Merging all the CSVs")
        merge_csvs("short")
        print("Adding averages across values for short MFD")
        add_value_averages("short", short_value_dictionary, short_mfd)

    if long:
        print("Getting ngrams for long MFD")
        ngrams(expanded_mfd)
        print("Merging all the CSVs")
        merge_csvs("long")
        print("Adding averages across values for long MFD")
        add_value_averages("long", long_value_dict, expanded_mfd)


