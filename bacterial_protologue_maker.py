#!/usr/bin/env python3

"""
bacterial_protologue_maker creates protologues from renamed and original GTDB metadata files

A program to create protologues for archaeal taxa using information from renamed and original GTDB metadata files
Outputs a file of traditional protologues in Rich Text Format.

USAGE:
    python3 archaeal_protologue_maker.py 

Needs as inputs in same directory:
    bac120_metadata_renamed.tsv
    bac120_metadata_r202.tsv

"""

__licence__ = 'GPLv3'
__author__ = 'Mark Pallen'
__author_email__ = 'mark.pallen@quadram.ac.uk'
__version__ = "0.0.1"

import os, sys, csv
import re
from operator import itemgetter
import codecs

## defines opening states of variables
renamed_phylogeny = []
original_phylogeny = []
renamed_phylogeny_tabbed = []
original_phylogeny_tabbed = []
reader_sorted = []
accession = []
genome_size = []
GC = []
file = []
gtdb_representative = []
gtdb_representative_species = []
ncbi_isolation_source = []
## reads in relevant columns from the renamed metadata file
with open("bac120_metadata_r207_renamed.tsv",encoding='latin-1') as renamed_metadata:
    next(renamed_metadata)
    for line in renamed_metadata:
      accession.append(line.split('\t')[0])
      renamed_phylogeny.append(line.split('\t')[16])
      genome_size.append(line.split('\t')[13])
      GC.append(line.split('\t')[12])
      ncbi_isolation_source.append(line.split('\t')[58])

      
##creates tab-delinated columns from the GTDB phylogeny entries
for line in renamed_phylogeny:
      renamed_phylogeny_tabbed.append(line.replace(";", "\t").replace(" ", "\t"))


## reads in relevant columns from the original metadata file
with open("./input_files/bac120_metadata_r207.tsv",encoding='latin-1') as original_metadata:
    next(original_metadata)
    for line in original_metadata:  
      original_phylogeny.append(line.split('\t')[16])

##creates tab-delinated columns from the GTDB phylogeny entries
for line in original_phylogeny:
      original_phylogeny_tabbed.append(line.replace(";", "\t").replace(" ", "\t"))


##merges the relevant columns from the two input files

merged = zip(renamed_phylogeny_tabbed, original_phylogeny_tabbed, accession, genome_size, GC, ncbi_isolation_source)

for a, b, c, d, e, f in merged: 
    file.append([a , b , c , d , e , f])


##sorts by new species names, then by new genus names
sortedfile = sorted(file, key=lambda file: file[0].split('\t')[7].replace("!", ""))
sortedfile = sorted(sortedfile, key=lambda file: file[0].split('\t')[5].replace("!", ""))

##opens the protologues file to be written to, with the .rtf extension and writes a header to make the file Rich Text Format
protologues = open("bacterial_protologues_for_classes.rtf", "w")
protologues.write("{\\rtf1")
protologues.write("\n")

##creates system for iterating through lines
previous_line = '\t'.join([''] * 20 ).split('\t') # 20 is set higher than the number of expected columns. 
for current_line_tabs in sortedfile:
  current_line = '\t'.join(current_line_tabs).split('\t')

## outputs a protologue for a newly named species
  
  if "!" in current_line[7]: 
      if current_line[7] not in previous_line[7]: ##ensures only first occurence of name acted on
          ## applies to newly named species with a genus name that contains an underscore, i.e. represents a genus split by GTDB with a suffix that cannot be used in a well-formed name
          ## outputs relevant protologue
          if "_" in current_line[5].replace("__", ""): 
            head, sep, tail = current_line[5].replace("g__", "").partition('_') ## splits the genus name from the suffix
            print \
            ("\\pard \\sa120 \\b Description of \i {\doccomm newname_6}Candidatus \i0" + head.replace("!", "").replace("g__", ""), current_line[7].replace("!", ""), "sp. nov.{\doccomm 6_newname} \\b0 \\par", \
            "\\pard \\sa120 \i Candidatus \i0", head.replace("!", "").replace("g__", ""), current_line[7].replace("!", ""), \
            "(N.L. fem. n. \i", current_line[7].replace("!", ""), "\i0 a species epithet created arbitrarily, while preserving the phonotactics and morphology of Latin; used as a noun in apposition). \\par", \
            "\\pard \\sa240 A species identified and delineated according to the algorithms of the Genome Taxonomy Database (GTDB) Release R207."\
            "The GTDB alphanumeric placeholder designation for this species is {\doccomm oldname_6}" + \
            current_line[13].replace("g__", ""), current_line[15].replace("!", "") + \
            "{\doccomm 6_oldname}\i0. Although GTDB has assigned a genus name with an alphabetic suffix, this genus designation cannot be incorporated into a well-formed binomial,"\
            " so in naming this species, we have used the basonym for the genus. The type genome for the species is the GenBank assembly", current_line[16].replace("GB_","") + \
            "\i0. The GC content of the type genome is",\
            round((float(current_line[18])), 2),\
            "% and the genome length is",\
            round((float((current_line[17]))/1000000),2), \
            "Mbp.", \
            file=protologues)
            if "none" not in current_line[19]:
              print (" The isolation source for the NCBI BioSample associated with the type genome is descibed as \""+ current_line[19] + "\".\\par", file=protologues)
            else:
              print ("\\par", file=protologues)
              
          else:
            print\
            ("\\pard \\sa120 \\b Description of \i {\doccomm newname_6}Candidatus \i0" + current_line[5].replace("g__", "").replace("!", ""), current_line[7].replace("!", ""), "sp. nov.{\doccomm 6_newname} \\b0 \\par", \
            "\\pard \\sa120 \i Candidatus \i0", current_line[6].replace("!", "").replace("s__", ""), current_line[7].replace("!", ""), \
            "(N.L. fem. n. \i", current_line[7].replace("!", ""), "\i0 a species epithet created arbitrarily, while preserving the phonotactics and morphology of Latin; used as a noun in apposition). \\par", \
            "\\pard \\sa240 A species identified and delineated according to the algorithms of the Genome Taxonomy Database (GTDB) Release R207."\
            " The GTDB alphanumeric placeholder designation for this species is {\doccomm oldname_6}" +  \
            current_line[13].replace("g__", ""), current_line[15].replace("!", "") + \
            "{\doccomm 6_oldname}\i0. The type genome for the species is the GenBank assembly", current_line[16].replace("GB_","") + \
            ". The GC content of the type genome is",\
            round((float(current_line[18])), 2),\
            "% and the genome length is",\
            round((float((current_line[17]))/1000000),2), \
            "Mbp.", \
            file=protologues)
            if "none" not in current_line[19]:  
                print (" The isolation source for the NCBI BioSample associated with the type genome is descibed as \""+ current_line[19] + "\".\\par", file=protologues)
            else:
              print ("\\par", file=protologues)

  ## outputs a protologue for a newly named genus                
  if "!" in current_line[5]: 
      if current_line[5] not in previous_line[5]:
          print \
          ("\\pard \\sa120 \\b Description of \i {\doccomm newname_5}Candidatus \i0" + current_line[5].replace("g__", "").replace("!", ""), "gen. nov.{\doccomm 5_newname} \\b0 \\par", \
          "\\pard \\sa120 \i Candidatus \i0", current_line[5].replace("!", "").replace("g__", ""), "(N.L. fem. n. \i", current_line[5].replace("!", "").replace("g__", ""),\
          "\i0 a name created arbitrarily, while preserving the phonotactics and morphology of Latin). \\par", \
          "\\pard \\sa120 A taxon identified and delineated according to the algorithms of the Genome Taxonomy Database (GTDB) Release R207."\
          " The GTDB alphanumeric placeholder designation for this genus is {\doccomm oldname_5}" +  \
          current_line[13].replace("g__", "") + \
           "{\doccomm 5_oldname}\i0. The type species for the genus is \i Candidatus \i0" + \
          current_line[5].replace("g__", "").replace("!", ""), current_line[7].replace("!", "") + ".\\par" \
          "\\pard \\sa480 According to the renamed version of GTDB Release R207, this genus belongs to the family", \
          "\i " + current_line[4].replace("f__", "").replace("!","") + "\i0. \\par", file=protologues)
        
  ## outputs a protologue for a newly named family
  if "!" in current_line[4]:
    if current_line[4].replace("f__", "").replace("aceae!", "a") in current_line[5].replace("g__", ""):
          if current_line[4] not in previous_line[4]:
            print \
            ("\\pard \\sa120 \\b Description of \i {\doccomm newname_4}Candidatus \i0" + current_line[4].replace("f__", "").replace("!", ""), "fam. nov.{\doccomm 4_newname} \\b0 \\par", \
            "\\pard \\sa120 \i Candidatus \i0", current_line[4].replace("!", "").replace("f__", ""), "(N.L. fem. pl. n. \i", current_line[4].replace("!", "").replace("f__", ""),\
            "\i0 a name created from the name of the type genus by addition of an appropriate suffix). \\par", \
            "\\pard \\sa120 A taxon identified and delineated according to the algorithms of the Genome Taxonomy Database (GTDB) Release R207."\
            " The GTDB alphanumeric placeholder designation for this taxon is {\doccomm oldname_4}" +  \
            current_line[12].replace("f__", "") + \
            "{\doccomm 4_oldname}.  The type genus for the taxon is \i Candidatus \i0" + \
            current_line[5].replace("g__", "").replace("!", "") + ".\\par"\
            "\\pard \\sa480 According to the renamed version of GTDB Release R207, this family belongs to the order \i " + current_line[3].replace("o__", "").replace("!","") + \
            "\i0. \\par",\
            file=protologues)

  ## outputs a protologue for a newly named order
  if "!" in current_line[3]: 
      if current_line[3].replace("o__", "").replace("ales!", "a") in current_line[5].replace("g__", ""): 
         if current_line[3] not in previous_line[3]:
            print \
            ("\\pard \\sa120 \\b Description of \i {\doccomm newname_3}Candidatus \i0" + current_line[3].replace("o__", "").replace("!", ""), "ord. nov.{\doccomm 3_newname} \\b0 \\par", \
            "\\pard \\sa120 \i Candidatus \i0", current_line[3].replace("!", "").replace("o__", ""), "(N.L. fem. pl. n. \i", current_line[3].replace("!", "").replace("o__", ""),\
            "\i0 a name created from the name of the type genus by addition of the appropriate suffix). \\par", \
            "\\pard \\sa120 A taxon identified and delineated according to the algorithms of the Genome Taxonomy Database (GTDB) Release R207."\
            " The GTDB alphanumeric placeholder designation for this taxon is {\doccomm oldname_3}" +  \
            current_line[11].replace("o__", "") + \
            "{\doccomm 3_oldname}.  The type genus for the taxon is \i Candidatus \i0" + \
            current_line[5].replace("g__", "").replace("!", "") + ".\\par"\
            "\\pard \\sa480 .According to the renamed version of GTDB Release R207, this order belongs to the class \i " + current_line[2].replace("c__", "").replace("!","") + \
            "\i0. \\par",\
            file=protologues)

  ## outputs a protologue for a newly named class
  if "!" in current_line[2]: 
      if current_line[2].replace("c__", "").replace("ia!", "a") in current_line[5].replace("g__", ""): 
        if current_line[2] not in previous_line[2]:
            print \
            ("\\pard \\sa120 \\b Description of \i {\doccomm newname_2}Candidatus \i0" + current_line[2].replace("c__", "").replace("!", ""), "class. nov.{\doccomm 2_newname} \\b0 \\par", \
            "\\pard \\sa120 \i Candidatus \i0", current_line[2].replace("!", "").replace("c__", ""), "(N.L. neut. pl. n. \i", current_line[2].replace("!", "").replace("c__", ""),\
            "\i0 a name created from the name of the type genus by addition of the appropriate suffix). \\par", \
            "\\pard \\sa120 A taxon identified and delineated according to the algorithms of the Genome Taxonomy Database (GTDB) Release R207."\
            " The GTDB alphanumeric placeholder designation for this taxon is {\doccomm oldname_2}" +  \
            current_line[10].replace("c__", "") + \
            "{\doccomm 2_oldname}.  The type order for the taxon is \i Candidatus \i0" + \
            current_line[3].replace("o__", "").replace("!", "") + ".\\par"\
            "\\pard \\sa480 According to the renamed version of GTDB Release R207, this class belongs to the phylum \i " + current_line[1].replace("p__", "").replace("!","") + \
            "\i0. \\par",\
            file=protologues)

  ## outputs protologue for newly named phylum
  if "!" in current_line[1]: 
      if current_line[1].replace("p__", "").replace("ota!", "a") in current_line[5].replace("g__", ""): 
       if current_line[1] not in previous_line[1]:
          print \
          ("\\pard \\sa120 \\b Description of \i {\doccomm newname_1}Candidatus \i0" + current_line[1].replace("p__", "").replace("!", ""), "phyl. nov.{\doccomm 1_newname} \\b0 \\par", \
          "\\pard \\sa120 \i Candidatus \i0", current_line[1].replace("!", "").replace("p__", ""), "(N.L. neut. pl. n. \i", current_line[1].replace("!", "").replace("p__", ""),\
          "\i0 a name created from the name of the type genus by addition of the appropriate suffix). \\par", \
          "\\pard \\sa120 A taxon identified and delineated according to the algorithms of the Genome Taxonomy Database (GTDB) Release R207."\
          " The GTDB alphanumeric placeholder designation for this taxon is {\doccomm oldname_1}" +  \
          current_line[9].replace("p__", "") + \
          "{\doccomm 1_oldname}.  The type genus for the taxon is \i Candidatus \i0" + \
          current_line[5].replace("g__", "").replace("!", "") + ".\\par"\
          "\\pard \\sa480 According to the renamed version of GTDB Release R207, this phylum belongs to the domain \i Archaea \i0" \
          ". \\par",\
          file=protologues)
                    
  previous_line = current_line #increments through lines

##closes RTF 
protologues.write("\n")
protologues.write("}")

