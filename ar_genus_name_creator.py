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
    "archa\n",
]


with open("excluded_terms.txt", "r", encoding="utf-8") as excluded_terms_handle:
    excluded_terms = dict.fromkeys([x.strip() for x in excluded_terms_handle.readlines()])

with open("genus_stems-good_names.txt", "r", encoding="utf-8") as compliant_stems:    
    for compliant_stem in compliant_stems:
        for ending in endings:
            compliant_stem = compliant_stem.replace("\n", "")
            names.append(f"{compliant_stem}{ending}")

random.shuffle(names)


names=sorted(names,key = lambda x:x[-2])
names.sort(key=len)

names_dict = dict.fromkeys([x.strip() for x in names])

with open("ar_excluded_genus_names.txt", "w", encoding="utf-8") as excluded_names_handle:
    with open("ar_genus_names.txt", "w", encoding="utf-8") as compliant_names_handle:
        for data in names_dict:
            if data in excluded_terms:
                data = data + "\n"
                excluded_names_handle.write(f"{data}")
            else:
                data = data + "\n"
                compliant_names_handle.write(f"{data}")
