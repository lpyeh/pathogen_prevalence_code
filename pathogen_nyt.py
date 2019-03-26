#!/usr/bin/python

import pandas as pd
import pickle
import os
import zipfile
import re
import pathlib
from collections import defaultdict
from collections import Counter
import csv

'''
Author: Leigh Yeh
Use the NYT corpus to find word frequency given words from the MFD.
'''
'''
# Only need to use this if zip files aren't extracted
def extract_zip():
    directory = 'txtOnly'
    os.chdir(directory)

    for zip_file in os.listdir(os.getcwd()):
        file_name = os.path.abspath(zip_file)
        zip_ref = zipfile.ZipFile(file_name)
        zip_ref.extractall(file_name)
        zip_ref.close()
        os.remove(file_name)
'''
pattern = re.compile('[\W_]+', re.UNICODE)


def get_nyt(dictionary, path, year_in):
    month_df = pd.DataFrame()
    for month in os.listdir(path):
        if not month.startswith('.'):
            print(month)
            month_path = os.path.join(path, month)
            frequency_dict = defaultdict(int)
            for file in os.listdir(month_path):
                if not file.startswith('.'):
                    file_path = os.path.join(month_path, file)
                    with open(file_path, encoding='utf-8-sig') as in_file:
                        in_file = pattern.sub(' ', in_file.read())
                        in_file = in_file.lower().strip()
                        # print(in_file)
                        wordcount = Counter(in_file.split())
                        for word in dictionary:
                            if word in wordcount:
                                frequency_dict[word] += wordcount[word]
                            else:
                                frequency_dict[word] += 0
            dataframe = pd.DataFrame(frequency_dict, index=[month])
            month_df = month_df.append(dataframe, sort=False)
    return month_df


if __name__ == '__main__':
    path = 'long_mfd.txt'
    mfd = open(path).read().lower().splitlines()
    mfd_df = pd.DataFrame()
    mfd = {k: 0 for k in mfd}
    year_list = []
    year_col = []
    os.chdir('NYT')

    for year in os.listdir(os.getcwd()):
        if not year.startswith('.') and not year.endswith('.pkl'):
            year_list.append(year)
            in_path = os.path.join(os.getcwd(), year)
            if in_path.endswith('.csv'):
                continue;
            df1 = get_nyt(mfd, in_path, year)
            mfd_df = mfd_df.append(df1)
        with open(year + '.pkl', 'wb') as out_file:
            pickle.dump(df1, out_file)
    year_col = [[x] * 12 for x in year_list]
    year_col = [a for b in year_col for a in b]

    mfd_df['Year'] = year_col

    mfd_df.to_csv("nyt_mfd_long.csv")
