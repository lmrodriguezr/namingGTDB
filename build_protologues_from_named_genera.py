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

## reads in relevant columns from the renamed taxonomy file
with open("ar53_taxonomy_r207_corrected.tsv",encoding='latin-1') as renamed_taxonomy:
    next(renamed_taxonomy)
    for line in renamed_taxonomy:
      renamed_phylogeny.append(line.split('\t')[1])
      
with open("bac120_taxonomy_r207_corrected.tsv",encoding='latin-1') as renamed_taxonomy:
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
sortedfile = sorted(sortedfile, key=lambda file: file[0].split('\t')[5].replace("@", ""))

##opens the protologues file to be written to, with the .rtf extension and writes a header to make the file Rich Text Format
protologues = open("protologues_built_from_named_genera.rtf", "w")
protologues.write("{\\rtf1")
protologues.write("\n")

##creates system for iterating through lines
previous_line = '\t'.join([''] * 20 ).split('\t') # 20 is set higher than the number of expected columns. 
for current_line_tabs in sortedfile:
  current_line = '\t'.join(current_line_tabs).split('\t')


  ## outputs a protologue for a newly named family
  if "@" in current_line[4]:
    target = current_line[4].replace("f__", "g__").replace("aceae", "").replace("@", "").replace("|", "").replace("|", "")
    target = target.rstrip(target[-1])
    if (target in current_line[5]) and ("_" not in current_line[5].replace("__","")) and (current_line[5] not in previous_line[5]):
        if "|" in current_line[4]:
          ##marker shows this is a Candidatus name    
            print \
            ("\\pard \\sa120 \\b Description of \i Candidatus \i0" + current_line[4].replace("f__", "").replace("@", "").replace("|", ""), "fam. nov. \\b0 \\par", \
            "\\pard \\sa120 \i Candidatus \i0", current_line[4].replace("@", "").replace("|", "").replace("f__", ""),\
            "(N.L. fem. pl. n. \i", current_line[4].replace("@", "").replace("|", "").replace("f__", ""),\
            "\i0 a name created from the name of the type genus by addition of an appropriate suffix).\\par", \
            "\\pard \\sa120 A taxon identified and delineated according to the algorithms of the Genome Taxonomy Database (GTDB) release R207.",\
             "The GTDB placeholder designation for this taxon is " +  \
            current_line[12].replace("f__", "") + \
            ". The type genus for the taxon is \i Candidatus \i0",\
            current_line[5].replace("g__", "").replace("@", "").replace("|", "") + ".\\par"\
            "\\pard \\sa480 According to the renamed version of GTDB release R207, this taxon belongs to the higher-level taxon \i " + current_line[3].replace("o__", "").replace("@", "").replace("|", "") + \
             "\i0.\\par",\
            file=protologues)

        else:
          ##is not a Candidatus name             
            print \
            ("\\pard \\sa120 \\b Description of \i " + current_line[4].replace("f__", "").replace("@", "").replace("|", ""), "\i0 fam. nov. \\b0 \\par", \
            "\\pard \\sa120\i", current_line[4].replace("@", "").replace("|", "").replace("f__", ""),
            "\i0(N.L. fem. pl. n. \i", current_line[4].replace("@", "").replace("|", "").replace("f__", ""),\
            "\i0 a name created from the name of the type genus by addition of an appropriate suffix).\\par", \
            "\i0\\pard \\sa120 A taxon identified and delineated according to the algorithms of the Genome Taxonomy Database (GTDB) release R207.",\
             "The GTDB placeholder designation for this taxon is " +  \
            current_line[12].replace("f__", "") + \
            ". The type genus for the taxon is \i",\
            current_line[5].replace("g__", "").replace("@", "").replace("|", "") + ".\i0\\par"\
            "\\pard \\sa480 According to the renamed version of GTDB release R207, this taxon belongs to the higher-level taxon \i " + current_line[3].replace("o__", "").replace("@", "").replace("|", "") + \
             "\i0.\\par",\
            file=protologues)
           

  ## outputs a protologue for a newly named order
  if "@" in current_line[3]:
    target = current_line[3].replace("o__", "g__").replace("ales", "").replace("@", "").replace("|", "").replace("|", "")
    target = target.rstrip(target[-1])
    if (target in current_line[5]) and ("_" not in current_line[5].replace("__","")) and (current_line[5] not in previous_line[5]):
        if "|" in current_line[3]:
          ##marker shows this is a Candidatus name    
            print \
            ("\\pard \\sa120 \\b Description of \i Candidatus \i0" + current_line[3].replace("o__", "").replace("@", "").replace("|", ""), "ord. nov. \\b0 \\par", \
            "\\pard \\sa120 \i Candidatus \i0", current_line[3].replace("@", "").replace("|", "").replace("o__", ""),\
            "(N.L. fem. pl. n. \i", current_line[3].replace("@", "").replace("|", "").replace("o__", ""),\
            "\i0 a name created from the name of the type genus by addition of an appropriate suffix).\\par", \
            "\\pard \\sa120 A taxon identified and delineated according to the algorithms of the Genome Taxonomy Database (GTDB) release R207.",\
             "The GTDB placeholder designation for this taxon is " +  \
            current_line[11].replace("o__", "") + \
            ". The type genus for the taxon is \i Candidatus \i0",\
            current_line[5].replace("g__", "").replace("@", "").replace("|", "") + ".\\par"\
            "\\pard \\sa480 According to the renamed version of GTDB release R207, this taxon belongs to the higher-level taxon \i " + current_line[2].replace("c__", "").replace("@", "").replace("|", "") + \
             "\i0.\\par",\
            file=protologues)

        else:
          ##is not a Candidatus name             
            print \
            ("\\pard \\sa120 \\b Description of \i " + current_line[3].replace("o__", "").replace("@", "").replace("|", ""), "\i0 ord. nov. \\b0 \\par", \
            "\\pard \\sa120\i", current_line[3].replace("@", "").replace("|", "").replace("o__", ""), "\i0(N.L. fem. pl. n. \i", current_line[3].replace("@", "").replace("|", "").replace("o__", ""),\
            "\i0 a name created from the name of the type genus by addition of an appropriate suffix).\\par", \
            "\i0\\pard \\sa120 A taxon identified and delineated according to the algorithms of the Genome Taxonomy Database (GTDB) release R207.",\
             "The GTDB placeholder designation for this taxon is " +  \
            current_line[11].replace("o__", "") + \
            ". The type genus for the taxon is \i",\
            current_line[5].replace("g__", "").replace("@", "").replace("|", "") + ".\i0\\par"\
            "\\pard \\sa480 According to the renamed version of GTDB release R207, this taxon belongs to the higher-level taxon \i " + current_line[2].replace("c__", "").replace("@", "").replace("|", "") + \
             "\i0.\\par",\
            file=protologues)
            
## outputs a protologue for a newly named class
  if "@" in current_line[2]:
    target = current_line[2].replace("c__", "g__").replace("ia@", "").replace("ia|", "").replace("|", "")
    target = target.rstrip(target[-1])
    if (target in current_line[5]) and ("_"  in current_line[5].replace("__", "")) and (current_line[5] not in previous_line[5]):
        if "|" in current_line[2]:
          ##marker shows this is a Candidatus name    
            print \
            ("\\pard \\sa120 \\b Description of \i Candidatus \i0" + current_line[2].replace("c__", "").replace("@", "").replace("|", ""), "class nov. \\b0 \\par", \
            "\\pard \\sa120 \i Candidatus \i0", current_line[2].replace("@", "").replace("|", "").replace("c__", ""),\
            "(N.L. neut. pl. n. \i", current_line[2].replace("@", "").replace("|", "").replace("c__", ""),\
            "\i0 a name created from the name of the type genus by addition of an appropriate suffix).\\par", \
            "\\pard \\sa120 A taxon identified and delineated according to the algorithms of the Genome Taxonomy Database (GTDB) release R207.",\
             "The GTDB placeholder designation for this taxon is " +  \
            current_line[1].replace("c__", "") + \
            ". The type genus for the taxon is \i Candidatus \i0",\
            current_line[5].replace("g__", "").replace("@", "").replace("|", "") + ".\\par"\
            "\\pard \\sa480 According to the renamed version of GTDB release R207, this taxon belongs to the higher-level taxon \i " + current_line[1].replace("p__", "").replace("@", "").replace("|", "") + \
             "\i0.\\par",\
            file=protologues)

        else:
          ##is not a Candidatus name             
            print \
            ("\\pard \\sa120 \\b Description of \i " + current_line[2].replace("c__", "").replace("@", "").replace("|", ""), "\i0 class nov. \\b0 \\par", \
            "\\pard \\sa120\i", current_line[2].replace("@", "").replace("|", "").replace("c__", ""),\
            "\i0(N.L. neut. pl. pl. n. \i", current_line[2].replace("@", "").replace("|", "").replace("c__", ""),\
            "\i0 a name created from the name of the type genus by addition of an appropriate suffix).\\par", \
            "\i0\\pard \\sa120 A taxon identified and delineated according to the algorithms of the Genome Taxonomy Database (GTDB) release R207.",\
             "The GTDB placeholder designation for this taxon is " +  \
            current_line[10].replace("c__", "") + \
            ". The type genus for the taxon is \i",\
            current_line[5].replace("g__", "").replace("@", "").replace("|", "") + ".\i0\\par"\
            "\\pard \\sa480 According to the renamed version of GTDB release R207, this taxon belongs to the higher-level taxon \i " + current_line[1].replace("p__", "").replace("@", "").replace("|", "") + \
             "\i0.\\par",\
            file=protologues)


## outputs a protologue for a newly named phylum
  if "@" in current_line[1]:
    target = current_line[1].replace("p__", "g__").replace("ota@", "").replace("ota|", "").replace("|", "").replace("@", "")
    target = target.rstrip(target[-1])
    if (target in current_line[5]) and ("_" not in current_line[5].replace("__","")) and (current_line[5] not in previous_line[5]):
        if "|" in current_line[1]:
          ##marker shows this is a Candidatus name    
            print \
            ("\\pard \\sa120 \\b Description of \i Candidatus \i0" + current_line[1].replace("p__", "").replace("@", "").replace("|", ""), "phyl. nov. \\b0 \\par", \
            "\\pard \\sa120 \i Candidatus \i0", current_line[1].replace("@", "").replace("|", "").replace("p__", ""),\
            "(N.L. neut. pl. n. \i", current_line[1].replace("@", "").replace("|", "").replace("p__", ""),\
            "\i0 a name created from the name of the type genus by addition of an appropriate suffix).\\par", \
            "\\pard \\sa120 A taxon identified and delineated according to the algorithms of the Genome Taxonomy Database (GTDB) release R207.",\
             "The GTDB placeholder designation for this taxon is " +  \
            current_line[9].replace("p__", "") + \
            ". The type genus for the taxon is \i Candidatus \i0",\
            current_line[5].replace("g__", "").replace("@", "").replace("|", "") + ".\\par"\
            "\\pard \\sa480 According to the renamed version of GTDB release R207, this taxon belongs to the higher-level taxon \i " + current_line[0].replace("d__", "").replace("@", "").replace("|", "") + \
             "\i0.\\par",\
            file=protologues)

        else:
          ##is not a Candidatus name             
            print \
            ("\\pard \\sa120 \\b Description of \i " + current_line[1].replace("p__", "").replace("@", "").replace("|", ""), "\i0 phyl. nov. \\b0 \\par", \
            "\\pard \\sa120\i", current_line[1].replace("@", "").replace("|", "").replace("p__", ""),\
            "\i0(N.L. neut. pl. n. \i", current_line[1].replace("@", "").replace("|", "").replace("p__", ""),\
            "\i0 a name created from the name of the type genus by addition of an appropriate suffix).\\par", \
            "\i0\\pard \\sa120 A taxon identified and delineated according to the algorithms of the Genome Taxonomy Database (GTDB) release R207.",\
             "The GTDB placeholder designation for this taxon is " +  \
            current_line[9].replace("p__", "") + \
            ". The type genus for the taxon is \i",\
            current_line[5].replace("g__", "").replace("@", "").replace("|", "") + ".\i0\\par"\
            "\\pard \\sa480 According to the renamed version of GTDB release R207, this taxon belongs to the higher-level taxon \i " + current_line[0].replace("d__", "").replace("@", "").replace("|", "") + \
             "\i0.\\par",\
            file=protologues)


  previous_line = current_line #increments through lines

##closes RTF 
protologues.write("\n")
protologues.write("}")


