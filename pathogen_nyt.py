#!/usr/bin/python

import pandas
import pickle
import os
import zipfile
import re
import pathlib
from collections import defaultdict
from collections import Counter

'''
Author: Leigh Yeh
Use the NYT corpus to find word frequency given words from the MFD.
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


def get_nyt(dictionary):
    frequency_dict = defaultdict(int)
    directory = 'NYT'
    os.chdir(directory)

    for year in os.listdir(os.getcwd()):
        for root, dirs, files in os.walk(year):
            for root2, dirs2, files2 in os.walk(root):
                root_path = os.path.abspath(root2)
                for file in files2:
                    file_path = os.path.join(root_path, file)
                    with open(file_path, 'rb') as f:
                        contents = f.read()
                        contents.decode()
                        print(contents)

if __name__ == '__main__':
    path = 'MFD.txt'
    mfd = open(path).read().lower().splitlines()
    d = ['this', 'is', 'a', 'test']
    get_nyt(d)



