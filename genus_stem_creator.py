#!/usr/bin/env python3
import random
import time
import logging
import argparse
import re
from os import path, getcwd
from shutil import copy

stems = []
stems_temp =[]


C1s = ["", "b", "c", "d", "f", "h", "l", "m", "s", "qu", "bl", "cl", "dr", "fl", "st", "ph"]
C2s = ["b", "c", "d", "f", "l", "m", "s", "x", "bl", "cl", "dr", "fr", "st"]
C3s = ["b", "c", "d", "f", "l", "m", "s", "x", "br", "cr", "dr", "fr",  "st"]
C = ["b", "c", "d", "f", "l", "m", "s", "x"]
Vs = ["a", "e", "i", "o", "u"]
b = ["b","p"]
f = ["f"]
c = ["c", "g"]
d = ["d", "t"]
m = ["m", "n"]
l = ["l", "r"]


for C1 in C1s:
    for C2 in C2s:
            for C3 in C3s:
                if (C2 not in C1) and (C3 not in C1) and (C2 not in C3) and (C3 not in C2):
                            if not ((C1 not in C) and (C3 not in C) and (C3 not in C)):
                                stems.append(f'{C1}{random.choice(Vs)}{C2}{random.choice(Vs)}{C3}')



with open("genus_stems.txt", "w", encoding="utf-8") as stems_out:
    stems = list(dict.fromkeys(stems))


    for data in stems:
            data = data.replace("quu", "qua").replace("b", random.choice(b)).replace("f", random.choice(f)).replace("c", random.choice(c)).replace("d", random.choice(d)).replace("m", random.choice(m)).replace("l", random.choice(l))
            stems_temp.append(data)
           
    random.shuffle(stems_temp)
    stems_temp = sorted (stems_temp, key = len)


    for data in stems_temp:
        stems_out.write(f"{data}\n")
