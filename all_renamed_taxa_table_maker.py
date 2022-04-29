#!/usr/bin/env python3
"""
this script creates protologues from named genera using corrected and original GTDB taxonomy files

A program to create protologues for archaeal and bacterial taxa using information from corrected and original GTDB taxonomy files
Outputs a file of traditional protologues in Rich Text Format.

USAGE:
    python3 build_protologues_from_named_genera.py 

Needs as inputs in same directory the renamed and original GTDB taxonomy files

"""

__licence__ = 'GPLv3'
__author__ = 'Mark Pallen'
__author_email__ = 'mark.pallen@quadram.ac.uk'
__version__ = "0.0.1"

import os, sys, csv
from operator import itemgetter
import codecs
import re

## defines opening states of variables
renamed_phylogeny = []
original_phylogeny = []
renamed_phylogeny_tabbed = []
original_phylogeny_tabbed = []
file = []
ar_names = []
bac_names = []
phylum_names = []

## reads in relevant columns from the renamed taxonomy file
with open("ar53_taxonomy_r207_corrected_all_renamed_marked.tsv",encoding='latin-1') as renamed_taxonomy:
    next(renamed_taxonomy)
    for line in renamed_taxonomy:
      renamed_phylogeny.append(line.split('\t')[1])
      
with open("bac120_taxonomy_r207_corrected_all_renamed_marked.tsv",encoding='latin-1') as renamed_taxonomy:
    next(renamed_taxonomy)
    for line in renamed_taxonomy:
      renamed_phylogeny.append(line.split('\t')[1])

##creates tab-delinated columns from the GTDB phylogeny entries
for line in renamed_phylogeny:
      renamed_phylogeny_tabbed.append(line.replace(";;",";").replace(";", "\t").replace(" ", "\t"))

## reads in relevant columns from the original taxonomy file
with open("ar53_taxonomy_r207.tsv",encoding='latin-1') as original_taxonomy:
    next(original_taxonomy)
    for line in original_taxonomy:  
      original_phylogeny.append(line.split('\t')[1])

## reads in relevant columns from the original taxonomy file
with open("bac120_taxonomy_r207.tsv",encoding='latin-1') as original_taxonomy:
    next(original_taxonomy)
    for line in original_taxonomy:  
      original_phylogeny.append(line.split('\t')[1])

##creates tab-delinated columns from the GTDB phylogeny entries
for line in original_phylogeny:
      original_phylogeny_tabbed.append(line.replace(";", "\t").replace(" ", "\t"))


##merges the relevant columns from the two input files

merged = zip(renamed_phylogeny_tabbed, original_phylogeny_tabbed)

for a, b in merged:
    file.append([a, b])


##sorts by new species names, then by new genus names
sortedfile = sorted(file)
sortedfile = sorted(sortedfile, key=lambda file: file[0].split('\t')[1].replace("@", ""))

##creates system for iterating through lines
previous_line = '\t'.join([''] * 20 ).split('\t') # 20 is set higher than the number of expected columns. 
for current_line_tabs in sortedfile:
  current_line = '\t'.join(current_line_tabs).split('\t')

  if "d__Archaea" in  current_line[0]:
    if "!" in current_line[1]:
            ar_names.append((current_line[9]) + "\t" +  (current_line[1]).replace("!","").replace("p__",""))  
    if "!" in current_line[2]:
            ar_names.append((current_line[10]) + "\t" +  (current_line[2]).replace("!","").replace("c__",""))  
    if "!" in current_line[3]:
            ar_names.append((current_line[11]) + "\t" +  (current_line[3]).replace("!","").replace("o__",""))  
    if "!" in current_line[4]:
            ar_names.append((current_line[12]) + "\t" +  (current_line[4]).replace("!","").replace("f__",""))  
    if "!" in current_line[5]:
            ar_names.append((current_line[13]) + "\t" +  (current_line[5]).replace("!","").replace("g__",""))  
    if "!" in current_line[7]:
            ar_names.append((((current_line[14] + " " + current_line[15]).replace("!","").strip() + "\t" + (current_line[6]).replace("!","").replace("s__","") + " " +  (current_line[7].replace("!","")))).strip())

  if "d__Bacteria" in  current_line[0]:
    if "!" in current_line[1]:
            bac_names.append((current_line[9]) + "\t" +  (current_line[1]).replace("!","").replace("p__",""))  
    if "!" in current_line[2]:
            bac_names.append((current_line[10]) + "\t" +  (current_line[2]).replace("!","").replace("c__",""))  
    if "!" in current_line[3]:
            bac_names.append((current_line[11]) + "\t" +  (current_line[3]).replace("!","").replace("o__",""))  
    if "!" in current_line[4]:
            bac_names.append((current_line[12]) + "\t" +  (current_line[4]).replace("!","").replace("f__",""))  
    if "!" in current_line[5]:
            bac_names.append((current_line[13]) + "\t" +  (current_line[5]).replace("!","").replace("g__",""))  
    if "!" in current_line[7]:
            bac_names.append((((current_line[14] + " " + current_line[15]).replace("!","").strip() + "\t" + (current_line[6]).replace("!","").replace("s__","") + " " +  (current_line[7].replace("!","")))).strip())

  previous_line = current_line #increments through lines

ar_names = list(dict.fromkeys(ar_names))
ar_names_sorted =  sorted(ar_names, key=lambda ar_names: ar_names.replace("p__", "1__").replace("c__", "2__").replace("o__", "3__").replace("f__", "4__").replace("g__", "5__").replace("s__", "6__"))

with open ("all_renamed_archaea_name_table.tsv", "w") as final_archaeal_names:
  for line in ar_names_sorted:
    final_archaeal_names.write((line.replace("p__","phylum\t").replace("c__","class\t")).replace("o__","order\t").replace("f__","family\t").replace("g__","genus\t").replace("s__","species\t") + "\n")
    if "p__" in line:
      phylum_names.append(line.split()[1])
      
bac_names = list(dict.fromkeys(bac_names))
bac_names_sorted =  sorted(bac_names, key=lambda bac_names: bac_names.replace("p__", "1__").replace("c__", "2__").replace("o__", "3__").replace("f__", "4__").replace("g__", "5__").replace("s__", "6__"))

with open ("all_renamed_bacteria_name_table.tsv", "w") as final_bacterial_names:
  for line in bac_names_sorted:
    final_bacterial_names.write((line.replace("p__","phylum\t").replace("c__","class\t")).replace("o__","order\t").replace("f__","family\t").replace("g__","genus\t").replace("s__","species\t") + "\n")
    if "p__" in line:
      phylum_names.append(line.split()[1])

phylum_names.sort()

with open ("phylum_name_table.tsv", "w") as phylum_name_table:
      for line in phylum_names:
          phylum_name_table.write(line + "\n")
          


