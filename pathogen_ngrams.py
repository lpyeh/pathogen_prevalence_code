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


'''
Returns a list of words from the Moral Foundations Dictionary website
'''
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


def add_value_averages(file_name):
    pd.read_csv(file_name)



if __name__ == '__main__':
    
    arg_string = ' '.join(sys.argv[1:]).lower()
    # params = [arg for arg in arg_string if arg.startswith('-')]
    
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
    base_words_path = "/Users/leigh/Desktop/pathogen_prevalence_code/MFD.txt"
    base_words = get_words(base_words_path)
    full_mfd = dictionary_text(mfd_url)
    # print(full_mfd)
    expanded_mfd = complete_dictionary(full_mfd)

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
        ngrams(base_words)
        print("Merging all the CSVs")
        merge_csvs("short")
    
    # merge_csvs("merged")
