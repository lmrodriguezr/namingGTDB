#!/usr/bin/env python3
"""
name_table_maker combines all opening word-components with all final word-components

A program to combine all opening word-components with all final word-components in 
the bacterial_genus_endings.txt, archaeal_genus_endings.txt and species_endings.txt 
files to create the output files bacterial_genus_names.txt, archaeal_genus_endings.txt 
and species_names.txt. The script then excluded genus names already been used in 
taxonomy by searching against the file GBIF_clean.txt, which contains a set of unique 
genus names compiled by the Global Biodiversity Information Facility.  

USAGE:
    python3 4_name_table_maker.py 

Needs as inputs in same directory:

"""

import re
import random
#import meta
import time
import logging 
import argparse
from os import path, getcwd

__licence__ = 'GPLv3'
__author__ = 'Mark Pallen'
__author_email__ = 'mark.pallen@quadram.ac.uk'
__other_authors__ = 'Nabil-Fareed Alikhan'
__version__ = "0.0.1"

epi = "Licence: " + __licence__ +  " by " +__author__ + " <" + __author_email__ + ">" + " with help from " + __other_authors__
logging.basicConfig()
log = logging.getLogger()


def containsNumber(value):
    """
    A simple method to check if there are any numbers in a string. 
    """
    return any([char.isdigit() for char in value])

def main(args):


    taxonomy_path = args.taxonomy_file
    input_names_path = args.input_names_file

    input_file_name = path.basename(input_names_path) # Retrieves the filename (to handle if given a file path as input)
    tax_file_name = path.basename(taxonomy_path)

    final_names_path = tax_file_name.replace("_taxonomy", "").replace(".tsv", "") + '_' + input_file_name.replace("unused_names_after_creating_ar122_species_names_table.txt", "bac_species_names").replace(".txt", "") + '_table.txt'  
    unused_names_path ='unused_names_after_creating_' + tax_file_name.replace("_taxonomy", "").replace(".tsv", "") + '_' + input_file_name.replace(".txt", "") + '_table.txt'

    species_names = {} # This stores original species names to be renamed and their frequency in the file. 

    taxa_names  = [] # This is used to store the original higher rank names 

    fields = ['accession', 'domain','phylum','class','order','family','genus','species_gen', 'species_spe']
    # all the input field in the taxonomy file (so it can be parsed)

    rank_names = ['domain','phylum','class','order','family','genus','species_gen']
    # This second list is the higher level ranks for genus mode. 

    taxon_pattern = re.compile("(.+)\td__(.+);p__(.+);c__(.+);o__(.+);f__(.+);g__(.+);s__(.+) (.+)")
    # Regex to extract all the values. 
    for field_name in rank_names:
    # in genus mode, values in higher ranks that need to be renamed are ordered by 
    # as they are found (line by line) and then by rank order. (domain, phylum -> genus)        
        with open(taxonomy_path) as taxonomy:            
            for line in taxonomy.readlines():
                # This is should be a taxonomy file 
                taxon_matches = taxon_pattern.search(line)
                if taxon_matches:
                    rank_values = dict(zip(fields, taxon_matches.group(1,2,3,4,5,6,7,8,9)))
                    # This merges the fields and the regex matches for each line to create a dictionary 
                    # This dictionary gives easy access to the value for each rank. e.g.  rank_values['order']
                    if args.genus: 
                        if re.findall('\d|-', rank_values[field_name]):
                            if rank_values[field_name] not in taxa_names:
                                taxa_names.append(rank_values[field_name])
                    else:
                        # Handles species renaming.
                        species_name = rank_values['species_spe']
                        if containsNumber(species_name): # species name should be sp[0-9] or something like that. 
                            if species_names.get(species_name): # If alpha nums has the name already, just increment the dictionary value (a counter)
                                species_names[species_name] += 1 
                            else: # Otherwise, add the name to the dictionary, count = 1. 
                                species_names[species_name] = 1                        
    if not args.genus: 
        # This is to create a list (sorted by frequency) for species mode (only). 
        taxa_names = [alphanum for alphanum, alphanum_freq in sorted(species_names.items(), key=lambda item: item[1], reverse=True)]
        
        
    gen_names = [x.strip() for x in open(input_names_path) ]


    with open(final_names_path, 'w') as file3:
        count = 0 # counter to step through the gen_names list as we go through taxa_names.
        
        for name in taxa_names:
            if args.genus: 
                print(name.strip(),'!' + gen_names[count].title(), file=file3)
                count += 1 # If there's more taxa_names values than genus names, this code will crash
            else:
                print(name.strip(),'!' + gen_names[count], file=file3)
                count += 1 # If there's more taxa_names values than genus names, this code will crash
        with open(unused_names_path, 'w') as unused_out:  # Write out unused names.
            unused_out.write('\n'.join(gen_names[count:] ))                     

if __name__ == '__main__':
    start_time = time.time()
    log.setLevel(logging.INFO)
    desc = __doc__.split('\n\n')[0].strip()
    parser = argparse.ArgumentParser(description=desc,epilog=epi)
    # Main parameters 
    parser.add_argument ('-v', '--verbose', action='store_true', default=False, help='verbose output')
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)
    parser.add_argument('-t', '--taxonomy_file', action='store', default='ar122_taxonomy.tsv', help='Taxonomy file')
    parser.add_argument('-g', '--genus', action='store_true', default=False, help='Format as genus names')     
    parser.add_argument('-i', '--input_names_file', action='store', default='input_names.txt', help='input_names_file')        
    parser.add_argument('-o', '--output_prefix', action='store', default='output', help='output file')

    args = parser.parse_args()
    if args.verbose: 
        log.setLevel(logging.DEBUG)
        log.debug( "Executing @ %s\n"  %time.asctime())    
    main(args)    
    if args.verbose: 
        log.debug("Ended @ %s\n"  %time.asctime())
        log.debug('total time in minutes: %d\n' %((time.time() - start_time) / 60.0))
