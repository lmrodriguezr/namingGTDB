#!/usr/bin/env python3
import random
import time
import logging
import argparse
import re
from os import path, getcwd
from shutil import copy

species_stems = []
compliant_species_stems = []
species_names =[]



cons1 = ["b",
"c", "d",
"f",
"g",
"l",
"m",
"n",
"p",
"r",
"s",
"t",
"v", "qu", "ph"]
cons2 = ["b",
"c", "d",
"f",
"g",
"l",
"m",
"n",
"p",
"r",
"s",
"t",
"v", "x", "ph"]
cons3 = ["b",
"c", "d",
"f",
"g",
"l",
"m",
"n",
"p",
"r",
"s",
"t",
"v", "x", "ph"]
vowels1 = ("a", "e", "i", "o", "u")
vowels2 = ("a", "e", "i", "o", "u")
vowels3 = ("a", "e", "i", "o", "u")
endings = [
    "ia\n",
    "ana\n",
    "osa\n",
    "aria\n",
    "ella\n",
]


for con1 in cons1:
    for con2 in cons2:
        for vowel1 in vowels1:   
                    if con1 != con2:
                        species_stems.append(f'{con1}{vowel1}{con2}')


for con1 in cons1:
    for con2 in cons2:
        for vowel1 in vowels1:
            for vowel2 in vowels2:    
                    if con1 != con2:
                        species_stems.append(f'{vowel1}{con1}{vowel2}{con2}')


for con1 in cons1:
    for con2 in cons2:
        for con3 in cons3:
            for vowel1 in vowels1:
                for vowel2 in vowels2:
                        if con1 != con2:
                            if con2 != con3:
                                if con1 != con3:
                                    species_stems.append(f'{con1}{vowel1}{con2}{vowel2}{con3}')


random.shuffle(species_stems)

species_stems=sorted(species_stems,key = lambda x:x[-2])
species_stems.sort(key=len)
species_stems = dict.fromkeys([x.strip() for x in species_stems])


with open("bac_genus_names.txt", "r", encoding="utf-8") as bac_genus_names_handle:
    bac_genus_names = dict.fromkeys([x.strip() for x in bac_genus_names_handle.readlines()])

with open("excluded_terms.txt", "r", encoding="utf-8") as excluded_terms_handle:
    excluded_terms = dict.fromkeys([x.strip() for x in excluded_terms_handle.readlines()])

with open("excluded_species_stems.txt", "w", encoding="utf-8") as excluded_stems_handle:
    for data in species_stems:
        if (data in excluded_terms) or (data in bac_genus_names) or "quu" in data:
            excluded_stems_handle.write(f"{data}\n")
        else:
            compliant_species_stems.append(data.strip())

for compliant_species_stem in compliant_species_stems:
    for ending in endings:
        species_names.append(f"{compliant_species_stem}{ending}".strip())

with open("excluded_species_names.txt", "w", encoding="utf-8") as excluded_species_names_handle:
    with open("species_names.txt", "w", encoding="utf-8") as compliant_species_names_handle:
        for data in species_names:
            if data in excluded_terms:
                excluded_species_names_handle.write(f"{data}\n")
            else:
                compliant_species_names_handle.write(f"{data}\n")
