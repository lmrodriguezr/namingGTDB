#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

"""
A program to replace GTDB alphanumeric placeholders with well-formed Latinate names in GTDB taxonomy files, ensuring that appropriate prefixes are added to names for higher-level taxa

USAGE:
    python3 batch-rename.py [options] -t <table.tsv> -i <text> -o <output-text>

Where:
    -t, --table <table.tsv>...    specifies as input a GTDB taxonomy file, either ar122_taxonomy.tsv or bac120_taxonomy.tsv
    -i, --input <input-text>      The input text file containing the patterns to replace
    -o, --output <output-text>    The output text file, if not specified the file will be printed to stdout

Examples:
    python3 taxon_renamer.py -g -t ar122_ar_genus_names_table.txt  -i ar122_taxonomy.tsv -o ar122_taxonomy_gen_renamed_marked.tsv
    python3 taxon_renamer.py -t ar122_species_names_table.txt  -i ar122_taxonomy_gen_renamed_marked.tsv -o ar122_taxonomy_all_renamed_marked.tsv
    python3 taxon_renamer.py -g -t bac120_bac_genus_names_table.txt  -i bac120_taxonomy.tsv -o bac120_taxonomy_gen_renamed_marked.tsv
    python3 taxon_renamer.py -t bac120_bac_species_names_table.txt -i bac120_taxonomy_gen_renamed_marked.tsv -o bac120_taxonomy_all_renamed_marked.tsv

"""

import os, sys
import logging 
import re 
import argparse
import time

__licence__ = 'GPLv3'
__author__ = 'Mark Pallen'
__author_email__ = 'mark.pallen@quadram.ac.uk'
__other_authors__ = 'Nabil-Fareed Alikhan + Andrea Telatin, QIB'
__version__ = "0.0.1"

epi = "Licence: " + __licence__ +  " by " +__author__ + " <" + __author_email__ + ">" + " with help from " + __other_authors__
logging.basicConfig()
log = logging.getLogger()

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def loadTermsTableFromFile(filename):
    """
    Loads a table from a two columns file (key, value)
    """
    terms = {}

    try:
        with open(filename, 'r') as f:
            for line in f:
                key, value = line.strip().split()
                terms[key] = value
                    
    except IOError as e:
        eprint("I/O error({0}): {1}\nWhile loading {2}".format(e.errno, e.strerror, filename))
        sys.quit(1)
    return terms
   
def read_taxon_file(input_file, output_file, replace, genus=False):
    with open(input_file, 'r') as f:
        output_lines = [] 
        fields = ['accession', 'domain','phylum','class','order','family','genus','species_gen', 'species_spe']
        taxon_pattern = re.compile("(.+)\td__(.+);p__(.+);c__(.+);o__(.+);f__(.+);g__(.+);s__(.+) (.+)")
        for line in f.readlines():
            # This is should be a taxonomy file 
            taxon_matches = taxon_pattern.search(line)
            if taxon_matches:
                rank_values = dict(zip(fields, taxon_matches.group(1,2,3,4,5,6,7,8,9)))
                if genus:
                    for rank, rank_value in rank_values.items():
                        new_value = replace.get(rank_value) 
                        if new_value:
                            if new_value.endswith('a'):
                                root = new_value[:-1] # clip off the ending 'a'
                                if rank == 'family':
                                    new_value = root + 'aceae!'
                                if rank == 'order':
                                    new_value = root + 'ales!'
                                if rank == 'class':
                                    new_value = root + 'ae!'
                                if rank == 'phylum':
                                    new_value = root + 'ota!'
                            elif new_value.endswith('um'):
                                root = new_value[:-2] # clip off the ending 'um'
                                if rank == 'family':
                                    new_value = root + 'aceae!'
                                if rank == 'order':
                                    new_value = root + 'ales!'
                                if rank == 'class':
                                    new_value = root + 'a!'
                                if rank == 'phylum':
                                    new_value = root + 'ota!'   
                            rank_values[rank] = new_value
                    
                else:
                    new_species = replace.get(rank_values['species_spe'], rank_values['species_spe'])
                    rank_values['species_spe'] = new_species
                output_string = rank_values['accession'] + '\t'
                output_string += ';'.join([x[0] + '__' +  rank_values[x] for x in fields[1:-2]])
                output_string += ';s__' + rank_values[fields[-2]]+ ' ' + rank_values[fields[-1]]
                output_lines.append(output_string)
            else:
                log.error('Could not read line ' + line )    
    output_handle = sys.stdout
    if output_file:
        output_handle = open(output_file, 'w')
    for line in output_lines:
        print(line, file=output_handle)

def read_metadata_file(input_file, output_file, replace, genus):
    # Load the input file
    try:
        with open(input_file, 'r') as f:
            text = f.read()
    except Exception as e:
        eprint(f"Error loading input file {input_file}: {e}")
        sys.exit(1)

    # Perform the replacements
    for key, value in replace.items():
        text = text.replace(("__" + key + ";"), ("__" + value + "!"))
        text = text.replace(("__" + key + " "), ("__" + value + "!"))
        text = text.replace((" " + key), (" " + value + "!"))

    # Write the output file

    with open(output_file, 'w') as f:
            f.write(text)


def main(args):
    # Load the table files
    replace = {}
    for table in args.table:
        if not os.path.exists(table):
            eprint("ERROR: Table file '{}' does not exist.".format(table))
            sys.exit(1)

        try:
            terms = loadTermsTableFromFile(table)
        except Exception as e:
            eprint(f"Error loading table {table}: {e}")
            sys.exit(1)
        eprint(f" - {table}: {len(terms)} terms")
        replace.update(terms)

    eprint(f" - Dictionary loaded with: {len(replace)} terms")

    # Load the input file
    is_metadata_file = False

    with open(args.input, 'r') as f:
        for line in f.readlines():
            if len(line.split('\t')) == 110: 
                is_metadata_file = True
            break
    if is_metadata_file:
        read_metadata_file(args.input, args.output, replace, args.genus)

    else: 
        read_taxon_file(args.input, args.output, replace, args.genus) 


   
if __name__ == '__main__':
    start_time = time.time()
    log.setLevel(logging.INFO)    
    parser = argparse.ArgumentParser(description='A program to replace patterns in text files using tables from tsv files (search, replace)')
    parser.add_argument ('-v', '--verbose', action='store_true', default=False, help='verbose output')
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)

    parser.add_argument('-t', '--table', help='table files', nargs="+", default=['ar_sp_name_table.txt'])
    parser.add_argument('-i', '--input', help='input file', default='ar122_taxonomy_r202.tsv')
    parser.add_argument('-o', '--output', help='output file')
    parser.add_argument('-g', '--genus', action='store_true', default=False, help='Rename genus (and higher) names')     


    args = parser.parse_args()


    if args.verbose: 
        log.setLevel(logging.DEBUG)
        log.debug( "Executing @ %s\n"  %time.asctime())    
    main(args)    
    if args.verbose: 
        log.debug("Ended @ %s\n"  %time.asctime())
        log.debug('total time in seconds: %d\n' %(time.time() - start_time))
