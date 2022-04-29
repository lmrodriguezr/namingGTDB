#!/usr/bin/env python3

import os, sys, csv
from operator import itemgetter
import codecs
import re


bac_names = []
ar_names = []
bac_tax = []
ar_tax = []
bac_anom_tax = []
ar_anom_tax = []

with open("bac120_taxonomy_r207.tsv", "r") as bac120:    
    for line in bac120:
            line1 = line.split(';s__')[0].replace("\n","")
            line2 = line1.split('\t')[1].replace("\n","")
            if not line.replace("_","").replace(";","").isalpha():
                bac_tax.append(line2)
            bac_names.append(line2.split(';')[5])
            if not line2.split(';')[1].replace("_","").replace(";","").isalpha():
                bac_names.append(line2.split(';')[1])
            if not line2.split(';')[2].replace("_","").replace(";","").isalpha():
                bac_names.append(line2.split(';')[2])
            if not line2.split(';')[3].replace("_","").replace(";","").isalpha():
                bac_names.append(line2.split(';')[3])
            if not line2.split(';')[4].replace("_","").replace(";","").isalpha():
                bac_names.append(line2.split(';')[4])

bac_names = list(dict.fromkeys(bac_names))
bac_tax = list(dict.fromkeys(bac_tax))

for line in bac_tax:
        if  line.split(';')[5].replace("_","").replace(";","").isalpha():
            if not line.split(';')[1].replace("_","").replace(";","").isalpha():
                bac_anom_tax.append((line.replace("p_","!p_") +  "\tAnomalous phylum" + "\t" +  (line.split(';')[1]) + ";"))
            if not line.split(';')[2].replace("_","").replace(";","").isalpha():
                bac_anom_tax.append((line.replace("c_","!c_") +  "\tAnomalous class" + "\t" + (line.split(';')[2]) + ";"))
            if not line.split(';')[3].replace("_","").replace(";","").isalpha():
                bac_anom_tax.append((line.replace("o_","!o_") + "\tAnomalous order" + "\t" + (line.split(';')[3])  + ";"))
            if not line.split(';')[4].replace("_","").replace(";","").isalpha():
                bac_anom_tax.append((line.replace("f_","!f_") +  "\tAnomalous family" + "\t" + (line.split(';')[4]) + ";" ))
 
        if not line.split(';')[1].replace("_","").replace(";","").isalpha():          
            if line.split(';')[1].replace("p_","g_") not in bac_names:
                bac_anom_tax.append((line.replace("p_","!p_") +  "\tAnomalous phylum" + "\t" +  (line.split(';')[1]) + ";"))
        if not line.split(';')[2].replace("_","").replace(";","").isalpha():
            if line.split(';')[2].replace("c_","g_") not in bac_names:
                bac_anom_tax.append((line.replace("c_","!c_") +  "\tAnomalous class" + "\t" + (line.split(';')[2]) + ";"))
        if not line.split(';')[3].replace("_","").replace(";","").isalpha():
            if line.split(';')[3].replace("o_","g_") not in bac_names:
                bac_anom_tax.append((line.replace("o_","!o_") + "\tAnomalous order" + "\t" + (line.split(';')[3])  + ";"))
        if not line.split(';')[4].replace("_","").replace(";","").isalpha():
            if line.split(';')[4].replace("f_","g_") not in bac_names:
                bac_anom_tax.append((line.replace("f_","!f_") +  "\tAnomalous family" + "\t" + (line.split(';')[4]) + ";" ))

bac_anom_tax.sort()
bac_anom_tax = list(dict.fromkeys(bac_anom_tax))

with open("bac_anomalous_name_table.tsv", "w") as bac_anom_taxa_out:
    bac_anom_taxa_out.write("Phylogeny\tRank\tAnomalous alphanumeric\n")
    for line in bac_anom_tax:
        bac_anom_taxa_out.write(line + "\n")

with open("ar53_taxonomy_r207.tsv", "r") as ar53:    
    for line in ar53:
            line1 = line.split(';s__')[0].replace("\n","")
            line2 = line1.split('\t')[1].replace("\n","")
            if not line.replace("_","").replace(";","").isalpha():
                ar_tax.append(line2)
            ar_names.append(line2.split(';')[5])
            if not line2.split(';')[1].replace("_","").replace(";","").isalpha():
                ar_names.append(line2.split(';')[1])
            if not line2.split(';')[2].replace("_","").replace(";","").isalpha():
                ar_names.append(line2.split(';')[2])
            if not line2.split(';')[3].replace("_","").replace(";","").isalpha():
                ar_names.append(line2.split(';')[3])
            if not line2.split(';')[4].replace("_","").replace(";","").isalpha():
                ar_names.append(line2.split(';')[4])

ar_names = list(dict.fromkeys(ar_names))
ar_tax = list(dict.fromkeys(ar_tax))

for line in ar_tax:
        if  line.split(';')[5].replace("_","").replace(";","").isalpha():
            if not line.split(';')[1].replace("_","").replace(";","").isalpha():
                ar_anom_tax.append((line.replace("p_","!p_") +  "\tAnomalous phylum" + "\t" +  (line.split(';')[1]) + ";"))
            if not line.split(';')[2].replace("_","").replace(";","").isalpha():
                ar_anom_tax.append((line.replace("c_","!c_") +  "\tAnomalous class" + "\t" + (line.split(';')[2]) + ";"))
            if not line.split(';')[3].replace("_","").replace(";","").isalpha():
                ar_anom_tax.append((line.replace("o_","!o_") + "\tAnomalous order" + "\t" + (line.split(';')[3])  + ";"))
            if not line.split(';')[4].replace("_","").replace(";","").isalpha():
                ar_anom_tax.append((line.replace("f_","!f_") +  "\tAnomalous family" + "\t" + (line.split(';')[4]) + ";" ))
 
        if not line.split(';')[1].replace("_","").replace(";","").isalpha():          
            if line.split(';')[1].replace("p_","g_") not in ar_names:
                ar_anom_tax.append((line.replace("p_","!p_") +  "\tAnomalous phylum" + "\t" +  (line.split(';')[1]) + ";"))
        if not line.split(';')[2].replace("_","").replace(";","").isalpha():
            if line.split(';')[2].replace("c_","g_") not in ar_names:
                ar_anom_tax.append((line.replace("c_","!c_") +  "\tAnomalous class" + "\t" + (line.split(';')[2]) + ";"))
        if not line.split(';')[3].replace("_","").replace(";","").isalpha():
            if line.split(';')[3].replace("o_","g_") not in ar_names:
                ar_anom_tax.append((line.replace("o_","!o_") + "\tAnomalous order" + "\t" + (line.split(';')[3])  + ";"))
        if not line.split(';')[4].replace("_","").replace(";","").isalpha():
            if line.split(';')[4].replace("f_","g_") not in ar_names:
                ar_anom_tax.append((line.replace("f_","!f_") +  "\tAnomalous family" + "\t" + (line.split(';')[4]) + ";" ))

ar_anom_tax.sort()
ar_anom_tax = list(dict.fromkeys(ar_anom_tax))

with open("ar_anomalous_names_table.tsv", "w") as ar_anom_taxa_out:
    ar_anom_taxa_out.write("Phylogeny\tRank\tAnomalous alphanumeric\n")
    for line in ar_anom_tax:
        ar_anom_taxa_out.write(line + "\n")
