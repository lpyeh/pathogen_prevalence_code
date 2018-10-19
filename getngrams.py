#!/usr/bin/env python
# -*- coding: utf-8 -*
from ast import literal_eval
from pandas import DataFrame  # http://github.com/pydata/pandas
import re
import requests               # http://github.com/kennethreitz/requests
import subprocess
import sys

corpora = dict(eng_us_2012=17, eng_us_2009=5, eng_gb_2012=18, eng_gb_2009=6,
               chi_sim_2012=23, chi_sim_2009=11, eng_2012=15, eng_2009=0,
               eng_fiction_2012=16, eng_fiction_2009=4, eng_1m_2009=1,
               fre_2012=19, fre_2009=7, ger_2012=20, ger_2009=8, heb_2012=24,
               heb_2009=9, spa_2012=21, spa_2009=10, rus_2012=25, rus_2009=12,
               ita_2012=22)


def getNgrams(query, corpus, startYear, endYear, smoothing, caseInsensitive):
    params = dict(content=query, year_start=startYear, year_end=endYear,
                  corpus=corpora[corpus], smoothing=smoothing,
                  case_insensitive=caseInsensitive)

    req = requests.get('http://books.google.com/ngrams/graph', params=params)
    res = re.findall('var data = (.*?);\\n', req.text)
    if res:
        data = {qry['ngram']: qry['timeseries']
                for qry in literal_eval(res[0])}
        df = DataFrame(data)
        df.insert(0, 'year', list(range(startYear, endYear + 1)))
    else:
        df = DataFrame()
    return req.url, params['content'], df


def runQuery(argumentString):
    arguments = argumentString.split()
    query = ' '.join([arg for arg in arguments if not arg.startswith('-')])
    
    params = [arg for arg in arguments if arg.startswith('-')]
    
       
    corpus, startYear, endYear, smoothing = 'eng_2012', 1800, 2008, 3
    caseInsensitive, allData = True, True
    toSave, toPrint, toPlot = True, False, False

    url, urlquery, df = getNgrams(query, corpus, startYear, endYear,
                                      smoothing, caseInsensitive)

    queries = urlquery.split(',')[0] + "-" + urlquery.split(',')[-1]
    filename = '%s-%d-%d.csv' % (queries, startYear,
                                              endYear)
    for col in df.columns:
        if '&gt;' in col:
            df[col.replace('&gt;', '>')] = df.pop(col)
        df.to_csv(filename, index=False)
    print('Data saved to ' + filename) 
        

def run(arguments):
    arg_string = ",".join(arguments)
    runQuery(arg_string)
