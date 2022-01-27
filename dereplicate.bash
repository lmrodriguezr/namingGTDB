#!/bin/bash

thr=80

# base=names_xl
# for base in genera_pa21 genera_icnp names_220113c ; do
for base in archaeal_genus_names_xl 2_3_string_names ; do
  echo "$base" >&2
  ./unique-soundex.r "${base}.txt" "${base}-sdx10.txt" "$thr" 10
  ./unique-soundex.r "${base}.txt" "${base}-sdx15.txt" "$thr" 15
  ./min-levenshtein.r "${base}-sdx15.txt" "${base}-sdx15-lev.tsv" "$thr"
  awk '$2 >= 3 { print $1 }' < "${base}-sdx15-lev.tsv" > "${base}-sdx15-lev.txt"
done

