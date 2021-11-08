#!/usr/bin/env python3
"""
name_creator create names for species and genera using combinations of openings and endings

A program to create names for species and genera using combinations of openings and endings from the input files.


USAGE:
    python3 name_creator.py [options] -p <list-of-name-openings-text> -e <list-of-name-endings-text>
    -g <specifies that genus names are being created> -x <excluded-terms-text> - o <output-file-text>

Where:
    -p --openings     opening word components for new taxonomic names, typically created by openings_creator.py
    -e --endings      final word components for new taxonomic names   
    -g --genus        specifies that names to be created are for the rank genus, ensuring capitalisation and sorting by complexity and length   
    -o --output_file  specifies the name of the output file
    -x --filter       specifies a file containing terms to be excluded from the output file

Examples:
    python3 name_creator.py -p name_openings.txt -e bac_genus_endings.txt -g -x excluded_terms.txt -o bac_genus_names.txt
    python3 name_creator.py -p name_openings.txt -e ar_genus_endings.txt -g -x excluded_terms.txt -o ar_genus_names.txt
    python3 name_creator.py -p name_openings.txt -e species_endings.txt -x excluded_terms.txt -o species_names.txt

"""

import random
import time
import logging 
import argparse
import re 
from os import path, getcwd
from shutil import copy

__licence__ = 'GPLv3'
__author__ = 'Mark Pallen'
__author_email__ = 'mark.pallen@quadram.ac.uk'
__other_authors__ = 'Nabil-Fareed Alikhan'
__version__ = "0.0.1"

epi = "Licence: " + __licence__ +  " by " +__author__ + " <" + __author_email__ + ">" + " with help from " + __other_authors__
logging.basicConfig()
log = logging.getLogger()

def generate_filter_list(list_of_files):
    all_ignore = set() 
    for file_name in list_of_files:
        for value in open(file_name).readlines():
            value = value.strip().lower()
            if value.isalpha():
                all_ignore.add(value)
    return all_ignore

def main(args):

    openings_path = args.openings
    endings_path = args.endings

    ignore_list_files = [] 
    if args.filter:
        ignore_list_files = args.filter

    curated_names_path = args.output_file 

    # Read in  values from each file into a list. Ensure does not read in blank lines by skippinglines less than 3 characters long. 
    openings = [line.strip() for line in open(openings_path) if len(line) >= 3 ]

    endings = [line.strip() for line in open(endings_path) if len(line) >= 3 ]
   
    combinations = [] # Create an empty list for opening/ending combinations
    
    for opening in openings:
        for ending in endings:
            if args.genus:
                opening_text = opening.capitalize()
            else:
                opening_text = opening
            combinations.append(f'{opening_text}{ending}')  #builds genus names and capitalises them
    random.shuffle(combinations)
 
    # Partitions list into a subset with no double consonants
    # and then a subset with double consonants,
    # so that simpler names are used first
    doubles = []    
    single = [] 
    pattern = re.compile(r"(?:(?![aeiou])[a-z]){2,}")
    for combination in combinations:
        double_conts = pattern.search(combination[0:5]) 
        if double_conts:
            doubles.append(combination)
        
                
        else: 
            single.append(combination)
            
    
    combinations = single + doubles # joins subsets together 
        

    # ensures there are no matches to the list of excluded terms
    # (e.g. head words from Wiktionary, previously used taxonomic names)
    # then writes to output file
    final_list = [] 
    if ignore_list_files:
        logging.debug('Building filter lists, as per files: '  + ', '.join(ignore_list_files))
        excluded_words = set(generate_filter_list(ignore_list_files))
        logging.debug('Loaded filter lists.')
        for data in combinations:
            data = data.strip().lower()
            if data not in excluded_words:
                if args.genus:
                    data = data.capitalize()
                    final_list.append(data)
                else:
                    final_list.append(data)
    else: 
        final_list = combinations
    with open(curated_names_path,'w') as curated_names_out:     
        curated_names_out.write('\n'.join(final_list))
    
    logging.debug('Done. Output to ' + curated_names_path)


if __name__ == '__main__':
    start_time = time.time()
    log.setLevel(logging.INFO)
    desc = __doc__.split('\n\n')[0].strip()
    parser = argparse.ArgumentParser(description=desc,epilog=epi)
    # Main parameters 
    parser.add_argument ('-v', '--verbose', action='store_true', default=False, help='verbose output')
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)
    parser.add_argument('-p', '--openings', action='store', default='stems.txt', help='opening stems from stem creator')
    parser.add_argument('-e', '--endings', action='store', default='species_endings.txt', help='endings file')    
    parser.add_argument('-g', '--genus', action='store_true', default=False, help='Format as genus names')     
    parser.add_argument('-o', '--output_file', action='store', default='curated_names.txt', help='output file')
    parser.add_argument('-x', '--filter', action='store', nargs='*', help='file paths to filter')
    args = parser.parse_args()
    if args.verbose: 
        log.setLevel(logging.DEBUG)
        log.debug( "Executing @ %s\n"  %time.asctime())    
    main(args)    
    if args.verbose: 
        log.debug("Ended @ %s\n"  %time.asctime())
        log.debug('total time in seconds: %d\n' %((time.time() - start_time) ))
