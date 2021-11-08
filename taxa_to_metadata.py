#!/usr/bin/env python3

"""
Updates a GTDB metadata file with a renamed GTDB taxonomy 

USAGE:
   python3 taxa_to_metadata.py

Where:
    -m, --metadata, an original GTDB metadata file, either ar122_metadata_r202.tsv or bac120_metadata_r202.tsv
    -i, --taxonomy',a renamed GTDB taxonomy file
    -o, --output', specifies the output file name

Examples:
    python3 taxa_to_metadata.py -m ar122_metadata_r202.tsv -i ar122_taxonomy_all_renamed_marked.tsv -o ar122_metadata_renamed.tsv
    python3 taxa_to_metadata.py -m bac120_metadata_r202.tsv -i bac120_taxonomy_all_renamed_marked.tsv -o bac120_metadata_renamed.tsv

"""

import os, sys
import logging 
import re 
import argparse
import time

__licence__ = 'GPLv3'
__author__ = 'Mark Pallen'
__author_email__ = 'mark.pallen@quadram.ac.uk'
__other_authors__ = 'Nabil-Fareed Alikhan'
__version__ = "0.0.1"

epi = "Licence: " + __licence__ +  " by " +__author__ + " <" + __author_email__ + ">" + " with help from " + __other_authors__
logging.basicConfig()
log = logging.getLogger()

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)



def main(args):
     # Make taxonomy dictionary 
    taxon = {}
    with open(args.taxonomy, 'r') as f:
        fields = ['accession', 'domain','phylum','class','order','family','genus','species_gen', 'species_spe']
        taxon_pattern = re.compile("(.+)\td__(.+);p__(.+);c__(.+);o__(.+);f__(.+);g__(.+);s__(.+) (.+)")
        for line in f.readlines():
            # This is should be a taxonomy file 
            taxon_matches = taxon_pattern.search(line)
            if taxon_matches:
                rank_values = dict(zip(fields, taxon_matches.group(1,2,3,4,5,6,7,8,9)))
                output_string = ';'.join([x[0] + '__' +  rank_values[x] for x in fields[1:-2]])
                output_string += ';s__' + rank_values[fields[-2]]+ ' ' + rank_values[fields[-1]]
                taxon[rank_values['accession']] = output_string
            else:
                log.error('Could not read line ' + line )    
    output_handle = sys.stdout
    if args.output:
        output_handle = open(args.output, 'w')
    with open(args.metadata, 'r') as f:    
        for line in f.readlines():
            current_line = line.strip().split('\t') 
            accession = current_line[0]
            if taxon.get(accession):
                current_line[16] = taxon[accession]
            print('\t'.join(current_line), file=output_handle)

   
if __name__ == '__main__':
    start_time = time.time()
    log.setLevel(logging.INFO)    
    parser = argparse.ArgumentParser(description='A program to replace patterns in text files using tables from tsv files (search, replace)')
    parser.add_argument ('-v', '--verbose', action='store_true', default=False, help='verbose output')
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)

    parser.add_argument('-m', '--metadata', help='metadata files', default="ar122_metadata_r202.tsv")
    parser.add_argument('-i', '--taxonomy', help='taxonomy file', default='ar122_taxonomy_r202.tsv')
    parser.add_argument('-o', '--output', help='output file', default = None)

    args = parser.parse_args()


    if args.verbose: 
        log.setLevel(logging.DEBUG)
        log.debug( "Executing @ %s\n"  %time.asctime())    
    main(args)    
    if args.verbose: 
        log.debug("Ended @ %s\n"  %time.asctime())
        log.debug('total time in seconds: %d\n' %(time.time() - start_time))
