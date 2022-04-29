#!/usr/bin/env python3

"""
input_terms_clean 

A program to clean up and collate input terms including Latin stems, wiktionary head words and previously used taxonomic names

USAGE:
    python3 input_terms_clean.py

Needs as inputs in same directory:
    STEMLIST.GEN: downloaded and extracted from http://archives.nd.edu/whitaker/old/wordsall.zip
    enwiktionary-latest-pages-articles-multistream-index.txt: downloaded and extracted from https://dumps.wikimedia.org/enwiktionary/latest/enwiktionary-latest-pages-articles-multistream-index.txt.bz2
    simple.txt: downloaded and extracted https://hosted-datasets.gbif.org/datasets/backbone/current/simple.txt.gz

"""

__licence__ = 'GPLv3'
__author__ = 'Mark Pallen'
__author_email__ = 'mark.pallen@quadram.ac.uk'
__version__ = "0.0.1"


input_terms = []

## extracts Latin stems from the relevant column in the input file

with open('STEMLIST.GEN', 'r') as input_file:     
    lines = input_file.readlines()
    for line in lines:
        input_terms.append(line.split(' ')[0].lower())

## extracts words from the relevant column in the input file, limiting to terms built from alphabetical ascii charcaters

with open('enwiktionary-latest-pages-articles-multistream-index.txt', 'r') as input_file:      
    lines = input_file.readlines()
    for line in lines:
        line = line.strip()
        if " " not in line:
                if line.split(":")[-1].isascii() and line.split(":")[-1].isalpha():
                    input_terms.append(line.split(":")[-1].lower())

## extracts taxonomic names from the relevant column in the input file
                    
with open('simple.txt', 'r') as input_file:
    for line in input_file:
        input_terms.append(line.split('\t')[20].lower())

#### sorts and dereplicates the list of stems

input_terms_list = list(dict.fromkeys(input_terms))
input_terms_list.sort()

## checks that they contain only alphabetical characters
## then writes to file

with open("excluded_terms.txt", "w") as output_file:
    for line in input_terms_list:
        if line.isalpha():
                output_file.write(f'{line}\n')

