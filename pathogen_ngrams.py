import requests
from collections import defaultdict
import re
import json
from ast import literal_eval

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


# Returns list of words to use as base words (AKA pathogen prevalence words)
def pathogen_text(path):
    pathogen_list = []
    return pathogen_list


# Gets list of all possible variations of word, given stem
def complete_dictionary(text_list):
    dictionary_path = "/Users/leigh/Desktop/words_dictionary.json"

    with open(dictionary_path) as words:
        words_dictionary = json.load(words)
        for text in text_list:
            for key in words_dictionary:
                if key.startswith(text):
                    text_list.append(key)


# getNgrams function, modified from https://github.com/encopy/google-ngrams
def getNgrams(query):
    eng_us_2012_corpus = 17
    params = dict(content = query, corpus=eng_us_2012_corpus, year_start=1800, year_end=2000)

    req = requests.get('http://books.google.com/ngrams/graph', params=params)
    res = re.findall('var data = (.*?);\\n', req.text)

    if res:
        data = {qry['ngram']: qry['timeseries'] for qry in literal_eval(res[0])}
        df = DataFrame(data)
        df.insert(0, 'year', list(range(year_start, year_end + 1)))
    else:
        df = DataFrame()

    return params['content'], df



# runQuery function, modified from https://github.com/encopy/google-ngram
def runQuery(string):
    filename = '%s-%s-%d-%d.csv' % (string, "eng_us_2012_corpus", 1800, 2000)
    urlquery, df = getNgrams(string)
    
    for col in df.columns:
        if '&gt;' in col:
            df[col.replace('&gt;', '>')] = df.pop(col)
        df.to_csv(filename, index=False)
        print('Data saved to %s' % filename)

    


if __name__ == '__main__':
    MFD_url = "https://www.moralfoundations.org/sites/default/files/files/downloads/moral%20foundations%20dictionary.dic"
    pathogen_path = "Put path here"

    target_words = dictionary_text(MFD_url)
    # base_words = pathogen_text(pathogen_path)
    complete_dictionary(target_words)
    query = ' '.join([word for word in target_words])
        

    print(target_words)
    
