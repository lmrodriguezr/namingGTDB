#!/usr/bin/env python3
import re

"""
GBIF_clean cleans up genus names from Global Biodiversity Information Facility (GBIF) input file

A program to extract genus from the backbone-current-simple.txt file downloaded from GBIF

USAGE:
    python3 GBIF_clean.py 

Needs as inputs in same directory:
    backbone-current-simple.txt

"""

__licence__ = 'GPLv3'
__author__ = 'Mark Pallen'
__author_email__ = 'mark.pallen@quadram.ac.uk'
__version__ = "0.0.1"

## extracts genus names from the relevant column in the input file
genuslist=[]

input_file = open('backbone-current-simple.txt', 'r')       

for line in input_file:
    genuslist.append(line.split('\t')[20])

input_file.close()

## sorts and dereplicates the list of genus names
genuslist=sorted(set(genuslist))

## converts all genus names to lower case
## checks that they contain only alphabetical characters
## then writes to file

output_file = open("GBIF_clean.txt", "w")

for value in genuslist: 
    value = value.lower()
    if value.isalpha(): 
        output_file.write(f'{value}\n')

output_file.close()
