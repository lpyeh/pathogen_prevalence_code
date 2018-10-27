# pathogen_prevalence_code

## Dependencies
_Requires Python version 3+_
Make sure to install the following:

* pickle
* pandas
* numpy
* requests
* dill
* gzip
* ahocorasick

Set the paths for (in pathogen_ngrams):

* base_words_path = path to file that stores the base words
* target_words_path = path to file that stores target words

Note: Both files must be a text file with each word on a new line

## Running
python pathogen_ngrams.py -optionalflag

optionalflag:
* -short: for the short version of MFD
* -long: for the long version of MFD
* -both: for both

If no flag is specified, short is the default

