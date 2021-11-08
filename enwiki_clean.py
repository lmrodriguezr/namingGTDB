#!/usr/bin/env python3
"""
enwiki_clean cleans up head words from the English Wiktionary

A program to extract head words from a file downloaded from the English Wiktionary

USAGE:
    python3 enwiki_clean.py 

Needs as inputs in same directory:
    enwiktionary-20210920-pages-articles-multistream-index.txt

"""

__licence__ = 'GPLv3'
__author__ = 'Mark Pallen'
__author_email__ = 'mark.pallen@quadram.ac.uk'
__version__ = "0.0.1"

## extracts head words from the relevant column in the input file
headwords=[]

input_file = open('enwiktionary-20210920-pages-articles-multistream-index.txt', 'r')       
lines = input_file.readlines()

for field in lines:
    headwords.append(field.split(':')[2])
input_file.close()

## sorts and dereplicates the list of head words
headwords=sorted(set(headwords))

## converts all headwords to lower case,
## checks that they contain only alphabetical characters,
## then writes to file
output_file = open("enwiki_terms.txt", "w")

for value in headwords: 
    value = value.strip().lower()
    if value.isalpha(): 
        output_file.write(f'{value}\n')

output_file.close()
