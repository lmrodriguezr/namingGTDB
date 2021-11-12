#!/usr/bin/env python3

"""
stemlist_clean cleans up stems from Whitaker's words

A program to extract Latin stems from the STEMSLIST.GEN file downloaded from Whitaker's words

USAGE:
    python3 stemlist_clean.py 

Needs as inputs in same directory:
    STEMLIST.GEN

"""

__licence__ = 'GPLv3'
__author__ = 'Mark Pallen'
__author_email__ = 'mark.pallen@quadram.ac.uk'
__version__ = "0.0.1"


## extracts stems from the relevant column in the input file
stemlist = []
input_file=open('STEMLIST.GEN', 'r')       

lines = input_file.readlines()
for fields in lines:
    stemlist.append(fields.split(' ')[0])

input_file.close()

## sorts and dereplicates the list of stems
stemlist=sorted(set(stemlist))

## converts all stems to lower case
## checks that they contain only alphabetical characters
## then writes to file
output_file = open("whitakers_stems.txt", "w")

for value in stemlist: 
    value = value.strip().lower()
    if value.isalpha(): 
        output_file.write(f'{value}\n')

output_file.close()
