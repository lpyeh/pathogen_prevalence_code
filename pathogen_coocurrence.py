import pickle
import os
from collections import defaultdict
import dill
import gzip
import pandas as pd
import numpy as np
import requests
import io
import sys


# Most of the code is from parallelGram | Author: Joe Hoover
# Code adapted to work with this project
def getFiles(ngram_path):
    ngram_files = []

    for f in os.listdir(ngram_path):
        if os.path.isfile(os.path.join(ngram_path, f)) and not f.startswitch('.'):
            ngram_files.append(f)
    return ngram_files


def getWords(word_path):
    with open(word_path, 'rb') as wf:
        words = [w.strip() for w in wf.readline().split(',')]
        return words


def mergeDicts(dict_list):
    union_dict = defaultdict(lambda: defaultdict(lambda: 0))

    for d in dict_list:
        for k1, v1, in d.items():
            for k2, v2 in v1.items():
                if type(v2) == int:
                    union_dict[k1][k2] += int(v2)

    return union_dict


def ngrams_cooccurrences(ngram_files, baseWords, targetWords, output_path, ngram_path):
    """
    This function using exact matching to identify co-occurrences.
    :param ngram_chunk: The files to search through for given job
    :param baseWords: List of base words
    :param targetWords: List of target words
    :param output_path: Where should results be stored?
    :param ngram_path: Where are the ngrams?
    :return: Nothing. Dumps results to pickeled file
    """
    wordFreqs = defaultdict(lambda: defaultdict(lambda: 0))
    coFreqs = defaultdict(lambda: defaultdict(lambda: 0))

    wordVols = defaultdict(lambda: defaultdict(lambda: 0))
    coVols = defaultdict(lambda: defaultdict(lambda: 0))

    file_counter = 0
    total_files = len(ngram_files) + 1

    for ngram_file in ngram_files:
        file_counter += 1
        print 'Analyzing file {0} of {1} in ngram_files'.format(file_counter, total_files)
        cur_file = gzip.open(os.path.join(ngram_path, ngram_file), 'rb')
        for line in cur_file:
            dat = line.split('\t')
            phrase = dat[0].lower()
            if any(baseWord in phrase for baseWord in baseWords):  # If contains baseword then
                if any(targetWord in phrase for targetWord in targetWords):  # If also contains target word, then
                    for bWord in baseWords:
                        if bWord in phrase:
                            wordFreqs[dat[1]][bWord] += int(dat[2])
                            wordVols[dat[1]][bWord] += int(dat[3].replace('\n', ''))

                            for tWord in targetWords:
                                if tWord in phrase:
                                    wordFreqs[dat[1]][tWord] += int(dat[2])
                                    wordVols[dat[1]][tWord] += int(dat[3].replace('\n', ''))
                                    coFreqs[dat[1]]['_'.join([bWord,tWord])] += int(dat[2])
                                    coVols[dat[1]]['_'.join([bWord,tWord])] += int(dat[3].replace('\n', ''))

                else:
                    for bWord in baseWords:
                        if bWord in phrase:
                            wordFreqs[dat[1]][bWord] += int(dat[2])
                            wordVols[dat[1]][bWord] += int(dat[3].replace('\n', ''))

            elif any(targetWord in phrase for targetWord in targetWords):
                    for tWord in targetWords:
                        if tWord in phrase:
                            wordFreqs[dat[1]][tWord] += int(dat[2])
                            wordVols[dat[1]][tWord] += int(dat[3].replace('\n', ''))

    dictFreqs = mergeDicts(dictList=[wordFreqs,coFreqs])
    dictVols = mergeDicts(dictList=[wordVols,coVols])
    ds = [dictFreqs, dictVols]

    print 'Writing {0}'.format(output_path)
    dill.dump(ds, open(output_path, 'wb'))


def main():
    ngram_path = "PUT PATH HERE"
    output_dir = "User/leigh/Desktop"
    # baseWordPath = "PUT PATH TO BASEWORDS HERE"
    targetWordPath = "PUT PATH TO TARGETWORDS HERE"
    output_path = output_dir + "/cooccurrence_dict.pkl"

    ngram_files = sorted(getFiles(ngram_path=ngram_path))
    target_words = getWords(targetWordPath)
    base_words = ['kindness', 'compassion', 'nurture', 'empathy', 'suffer', 'cruel', 'hurt', 'harm',
                  'fairness', 'equality', 'justice', 'rights', 'cheat', 'fraud', 'unfair','injustice',
                  'loyal', 'solidarity', 'patriot', 'fidelity', 'betray', 'treason', 'disloyal', 'traitor',
                  'authority', 'obey', 'respect', 'tradition', 'subversion', 'disobey', 'disrespect', 'chaos',
                  'purity', 'sacred', 'wholesome', 'impurity', 'depravity', 'degradation', 'unnatural']

    ngrams_cooccurrences(ngram_files, base_words, target_words, output_path, ngram_path)
    
    

if __name__=='__main__':
    main()
