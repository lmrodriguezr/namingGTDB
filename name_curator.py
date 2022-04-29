#!/usr/bin/env python3.8

"""
leven_names compares a text file of names against themselves to filter by Levenshtein distance. 
Requires python-Levenshtein and Fuzzy
pip install python-Levenshtein
pip install Fuzzy
### CHANGE LOG ### 
2022-01-12 Nabil-Fareed Alikhan <nabil@happykhan.com>
    * Initial build
"""
from Levenshtein import distance
import time 
import logging 
import sys 
import argparse 
from fuzzy import Soundex, DMetaphone, nysiis
import unicodedata

__licence__ = 'GPLv3'
__author__ = 'Nabil-Fareed Alikhan'
__author_email__ = 'nabil@happykhan.com'
__version__ = "1.0.2"

epi = "Licence: " + __licence__ +  " by " +__author__ + " <" +__author_email__ + ">"

logging.basicConfig(format='%(asctime)s (%(levelname)s): %(message)s')
log = logging.getLogger()


def _refined_soundex(s, count_cutoff = 4):
    # Modifed from jellyfish module. 
    if not s:
        return ""

    s = unicodedata.normalize("NFKD", s)
    s = s.upper()

    replacements = (
        ("BFPV", "1"),
        ("PV", "2"),
        ("CKS", "3"),
        ("GJ", "4"),
        ("QXZ", "5"),
        ("DT", "6"),
        ("L", "7"),
        ("MN", "8"),
        ("R", "9"),
    )
    result = [s[0]]
    count = 1

    # find would-be replacment for first character
    for lset, sub in replacements:
        if s[0] in lset:
            last = sub
            break
    else:
        last = None

    for letter in s[1:]:
        for lset, sub in replacements:
            if letter in lset:
                if sub != last:
                    result.append(sub)
                    count += 1
                last = sub
                break
        else:
            if letter != "H" and letter != "W":
                # leave last alone if middle letter is H or W
                last = None
        if count == count_cutoff:
            break

    result += "0" * (count_cutoff - count)
    return "".join(result)


def _leven_compare(list1, list2, minimal_distance_cutoff=1, run_phono=False):
    accept = []
    reject = []
    if run_phono == 'nysiis':
        phono_method = nysiis()
    elif run_phono == 'metaphone':
        phono_method = DMetaphone()
    elif run_phono == 'relaxed_soundex':
        phono_method = _refined_soundex(15)
    else:
        phono_method = Soundex(15)
    total_collisions = 0
    for ele in list1:
        ele = ele.strip()
        minimal_distance = 1000000
        for ele2 in list2:
            ele2 = ele2.strip()
            if ele != ele2: 
                if run_phono == 'metaphone':
                    dist = distance(phono_method(ele)[0], phono_method(ele2)[0])
                elif run_phono:
                    dist = distance(phono_method(ele), phono_method(ele2))
                else:
                    dist = distance(ele, ele2)
                
                if dist < minimal_distance:
                    minimal_distance = dist     
                if dist < minimal_distance_cutoff:
                    log.debug(f'collision {ele} - {ele2}: {dist}')
                    total_collisions += 1
        if minimal_distance >= minimal_distance_cutoff:
            accept.append(ele)
        else:
            reject.append(ele)
    log.debug(f'Total collisions: {total_collisions}')
    return accept, reject

def main(args):
    
    with open(args.namelist) as f:
        names = dict.fromkeys(f.readlines())
        good_name_path = args.output_prefix + '-good_names.txt'
        reject_name_path = args.output_prefix + '-rejected_names.txt'
        
        if args.sound:   
            good_name_path = args.output_prefix + '-good_names_sound.txt'
            reject_name_path = args.output_prefix + '-rejected_name_sound.txt'            

        logging.info('Writing good names to ' + good_name_path)
        logging.info('Writing rejected  names to ' + reject_name_path)

        accept, reject = _leven_compare(names, names, int(args.cutoff), args.sound)
        open(good_name_path ,'w').write('\n'.join(accept))
        open(reject_name_path,'w').write('\n'.join(reject))

        
if __name__ == '__main__':

    start_time = time.time()
    log.setLevel(logging.INFO)
    desc = __doc__.split('\n\n')[0].strip()
    parser = argparse.ArgumentParser(description=desc,epilog=epi)
    parser.add_argument ('-v', '--verbose', action='store_true', default=False, help='verbose output')
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)
    parser.add_argument('namelist', action='store', help='Text file with list of names to compare, one per line' )  
    parser.add_argument('--cutoff', action='store', default=3, help='Distance on which to filter, minimal distance should be greater than or equal to this, default: 3 ' )
    parser.add_argument('--output_prefix', action='store', default='levfilter', help='Output prefix for files' )
    parser.add_argument('--sound', action='store', default=None, choices=['soundex', 'refined_soundex', 'metaphone', 'nysiis'], help='Pre-process using a phonetic algorithms (soundex, refined_soundex, metaphone, nysiis). No preprocessing by default' )


    args = parser.parse_args()

    if args.verbose: 
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug( "Executing @ %s\n"  %time.asctime())    

    main(args)

    if args.verbose: 
        logging.debug("Ended @ %s\n"  %time.asctime())
        logging.debug('total time in minutes: %d\n' %((time.time() - start_time) / 60.0))
    sys.exit(0)
