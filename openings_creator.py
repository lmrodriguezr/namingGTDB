#!/usr/bin/env python3
"""
openings_creator creates 5-letter arbitrary meaningless opening word-components that comply with the phonotactics of Latin

A program to create 5-letter arbitrary meaningless opening word-components that comply with the phonotactics of Latin
that are not present in a set of excluded terms (e.g.head words from the English wiktionary, which also contains words from Latin and many other languages)
and that do not contain tandem vowels or clusters of more than 2 consonants or strings with unwanted connatations (e.g. vulgarities)

USAGE:
    python3 openings_creator.py

Where:
    -i', --terms, specifies output file, default='whitakers_stems.txt', created by stemlist_clean.py
    -o', --output_file, specifies output file,  default='openings.txt'
    -x', --filter', specifies file with excluded terms

Example:
    python3 openings_creator.py -i whitakers_stems.txt -x excluded_terms.txt -o name_openings.txt

"""

import re, random
import time
import logging 
import argparse
from os import path

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

def check_input(stems_path):
    if not path.exists(stems_path):
        logging.error(f'No file found in {stems_path}')
        exit()
    return True

def main(args):

    stems_path = args.terms
    output_path = args.output_file

    ignore_list_files = [] 
    if args.filter:
        ignore_list_files = args.filter
    ignore_list_files =  list(set(ignore_list_files + [args.terms]))
    logging.debug('Ignoring values listed in ' + ','.join(ignore_list_files))
    if check_input(stems_path):
        logging.debug('Input ok, generating stems...')
        stems_tmp = []
        uniq_stems = []

        #opens file of Latin stems, selects opening 5-letter strings ending in classical Latin consonants, removes strings with unwanted components
        logging.debug('Creating stems from input file...')
        with open(stems_path, 'r') as stems_in:
            for line in stems_in:
                if len(line) >= 6:
                    if re.search ('b|c|d|f|g|l|m|n|p|r|s|t|v|x|z', line[4]):
                        if not re.search('[aeiou][aeiou]|[b-df-hj-np-tv-z][b-df-hj-np-tv-z][b-df-hj-np-tv-z]|j|k|w|z|[A-Z]|zm|rh|thm|sex|arse|bum|inebr|tit',line):
                            stems_tmp.append(line[0:5])

        #creates a dictionary to dereplicate the list of strings, then randomly shuffles them
        logging.debug('Dereplicating and shuffling...')
        selected_stems = list(stems_tmp)
        uniq_selected_stems_list = list(dict.fromkeys(selected_stems))
        random.shuffle(uniq_selected_stems_list)
        for line in uniq_selected_stems_list:
            if not re.search('[b-df-hj-np-tv-z][b-df-hj-np-tv-z]',line):
                uniq_stems.append(line.strip())

        for line in uniq_selected_stems_list:      
            if re.search('[b-df-hj-np-tv-z][b-df-hj-np-tv-z]',line):
                uniq_stems.append(line.strip())

        #opens one or more files of excluded terms
        #removes any matches from the list of 5-letter strings and outputs a list of suitable opening word-components
        logging.debug('Creating filter lists...')
        ignore_set = generate_filter_list(ignore_list_files)
        logging.debug('Filtering stems...')
        with open(output_path,'w') as stems_out: 
            for data in uniq_stems:
                if data.lower() not in ignore_set:
                    stems_out.write(f'{data}\n')
        logging.debug('Done. Output to ' + output_path)


if __name__ == '__main__':
    start_time = time.time()
    log.setLevel(logging.INFO)
    desc = __doc__.split('\n\n')[0].strip()
    parser = argparse.ArgumentParser(description=desc,epilog=epi)
    # Main parameters 
    parser.add_argument ('-v', '--verbose', action='store_true', default=False, help='verbose output')
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)
    parser.add_argument('-i', '--terms', action='store', default='whitakers_stems.txt', help='whitakers stems')
    parser.add_argument('-o', '--output_file', action='store', default='openings.txt', help='output file')
    parser.add_argument('-x', '--filter', action='store', nargs='*', help='file paths to filter')
    args = parser.parse_args()
    if args.verbose: 
        log.setLevel(logging.DEBUG)
        log.debug( "Executing @ %s\n"  %time.asctime())    
    main(args)    
    if args.verbose: 
        log.debug("Ended @ %s\n"  %time.asctime())
        log.debug('total time in minutes: %d\n' %((time.time() - start_time) / 60.0))
