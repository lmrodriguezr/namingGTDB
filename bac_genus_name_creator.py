#!/usr/bin/env python3
import random
import time
import logging
import argparse
import re
from os import path, getcwd
from shutil import copy

names = []
endings = [
    "ia\n",
    "ana\n",
    "osa\n",
    "aria\n",
    "ella\n",
    "astra\n",
    "atica\n",
    "entia\n",
    "etta\n",
    "ibra\n",
    "ibula\n",
    "icella\n",
    "ifica\n",
    "iforma\n",
    "igena\n",
    "ilega\n",
    "ilenta\n",
    "isca\n",
    "itia\n",
    "itoga\n",
    "itura\n",
    "ivita\n",
    "ousia\n"
]

with open("excluded_terms.txt", "r", encoding="utf-8") as excluded_terms_handle:
    excluded_terms = dict.fromkeys([x.strip() for x in excluded_terms_handle.readlines()])

with open("genus_stems-good_names.txt", "r", encoding="utf-8") as compliant_stems:    
    for compliant_stem in compliant_stems:
        for ending in endings:
            compliant_stem = compliant_stem.replace("\n", "")
            names.append(f"{compliant_stem}{ending}")


names = dict.fromkeys([x.strip() for x in names])
names = sorted(names,key = lambda x:x[-2])
names = sorted(names, key=len)




with open("bac_excluded__genus_names.txt", "w", encoding="utf-8") as excluded_names_handle:
    with open("bac_genus_names.txt", "w", encoding="utf-8") as compliant_names_handle:
        for data in names:
            if data in excluded_terms:
                data = data + "\n"
                excluded_names_handle.write(f"{data}")
            else:
                data = data + "\n"
                compliant_names_handle.write(f"{data}")
