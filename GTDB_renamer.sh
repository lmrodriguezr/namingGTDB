## GTDB renamer shell script

##enable python scripts to run
chmod u+x *py
##
##download and parse Whitaker's stems
mkdir whitakers_words
wget http://archives.nd.edu/whitaker/wordsall.zip
unzip wordsall.zip -d whitakers_words
rm wordsall.zip
mv whitakers_words/STEMLIST.GEN ./
rm -d -r whitakers_words
./stemlist_clean.py
rm STEMLIST.GEN
##
##download and parse English Wiktionary head words
wget https://dumps.wikimedia.org/enwiktionary/20210920/enwiktionary-20210920-pages-articles-multistream-index.txt.bz2
bzip2 -d enwiktionary-20210920-pages-articles-multistream-index.txt.bz2
./enwiki_clean.py 
rm enwiktionary-20210920-pages-articles-multistream-index.txt
##
##download and parse genus names already in use
wget https://hosted-datasets.gbif.org/datasets/backbone/backbone-current-simple.txt.gz
gunzip backbone-current-simple.txt.gz
./GBIF_clean.py
rm backbone-current-simple.txt
##
##create a single file of excluded terms
cat whitakers_stems.txt enwiki_terms.txt GBIF_clean.txt > excluded_terms.txt
##
##download and decompress GTDB taxonomy and metadata files
wget https://data.gtdb.ecogenomic.org/releases/latest/ar122_taxonomy.tsv.gz
wget https://data.gtdb.ecogenomic.org/releases/latest/ar122_metadata.tar.gz
wget https://data.gtdb.ecogenomic.org/releases/latest/bac120_metadata.tar.gz
wget https://data.gtdb.ecogenomic.org/releases/latest/bac120_taxonomy.tsv.gz
tar -xvzf bac120_metadata.tar.gz 
tar -xvzf ar122_metadata.tar.gz
gunzip bac120_taxonomy.tsv.gz ar122_taxonomy.tsv.gz
rm *.gz
##
##run the scripts to create names and use them to replace alphanumeric placeholders in GTDB files
./openings_creator.py -i whitakers_stems.txt -x excluded_terms.txt -o name_openings.txt
./name_creator.py -p name_openings.txt -e bac_genus_endings.txt -g -x excluded_terms.txt -o bac_genus_names.txt
./name_creator.py -p name_openings.txt -e ar_genus_endings.txt -g -x excluded_terms.txt -o ar_genus_names.txt
./name_creator.py -p name_openings.txt -e species_endings.txt -x excluded_terms.txt -o species_names.txt
./name_table_maker.py -g -t ar122_taxonomy.tsv -i ar_genus_names.txt
./name_table_maker.py -g -t bac120_taxonomy.tsv -i bac_genus_names.txt 
./name_table_maker.py -t ar122_taxonomy.tsv -i species_names.txt 
./name_table_maker.py -t bac120_taxonomy.tsv -i unused_names_after_creating_ar122_species_names_table.txt
./taxon_renamer.py -g -t ar122_ar_genus_names_table.txt  -i ar122_taxonomy.tsv -o ar122_taxonomy_gen_renamed_marked.tsv
./taxon_renamer.py -t ar122_species_names_table.txt  -i ar122_taxonomy_gen_renamed_marked.tsv -o ar122_taxonomy_all_renamed_marked.tsv
./taxon_renamer.py -g -t bac120_bac_genus_names_table.txt  -i bac120_taxonomy.tsv -o bac120_taxonomy_gen_renamed_marked.tsv
./taxon_renamer.py -t bac120_bac_species_names_table.txt -i bac120_taxonomy_gen_renamed_marked.tsv -o bac120_taxonomy_all_renamed_marked.tsv

./taxon_renamer.py -g -t ar122_ar_genus_names_table.txt  -i gtdb_taxonomy.tsv -o gtdb_ar_gen_renamed_marked.tsv
./taxon_renamer.py -t ar122_species_names_table.txt  -i gtdb_ar_gen_renamed_marked.tsv -o gtdb_ar_all_renamed_marked.tsv
./taxon_renamer.py -g -t bac120_bac_genus_names_table.txt  -i gtdb_ar_all_renamed_marked.tsv -o gtdb_ar_all_bac_gen_renamed_marked.tsv
./taxon_renamer.py -t bac120_bac_species_names_table.txt -i gtdb_ar_all_bac_gen_renamed_marked.tsv -o gtdb_taxonomy_renamed_marked.tsv



sed 's/[!]//g' ar122_taxonomy_all_renamed_marked.tsv > ar122_taxonomy_all_renamed_unmarked.tsv
sed 's/[!]//g' bac120_taxonomy_all_renamed_marked.tsv > bac120_taxonomy_all_renamed_unmarked.tsv
sed 's/[!]//g' gtdb_taxonomy_renamed_marked.tsv > gtdb_taxonomy_renamed_unmarked.tsv

./taxa_to_metadata.py -m ar122_metadata_r202.tsv -i ar122_taxonomy_all_renamed_marked.tsv -o ar122_metadata_renamed.tsv
./taxa_to_metadata.py -m bac120_metadata_r202.tsv -i bac120_taxonomy_all_renamed_marked.tsv -o bac120_metadata_renamed.tsv
## create the protologues and name tables
./archaeal_protologue_maker.py
./bacterial_protologue_maker.py
grep -o 'newname_.*_newname' archaeal_protologues.rtf | sed "s/newname_//" | sed "s/nov.*newname/nov\./" | sed "s/\\\i0//" | sed "s/.Candidatus/Candidatus/" > new_ar_names.txt
grep -o 'oldname_.*_oldname' archaeal_protologues.rtf | sed "s/oldname_//" | sed "s/[{].*//" | sed "s/\\\i0//" > old_ar_names.txt
paste -d,  new_ar_names.txt old_ar_names.txt  | sort  | sed "s/.Candidatus/Candidatus/"  | sed "s/.[}]//" > ar122_r202_name_table.csv
grep -o 'newname_.*_newname' bacterial_protologues.rtf | sed "s/newname_//" | sed "s/nov.*newname/nov\./" | sed "s/\\\i0//" | sed "s/.Candidatus/Candidatus/" > new_bac_names.txt
grep -o 'oldname_.*_oldname' bacterial_protologues.rtf | sed "s/oldname_//" | sed "s/[{].*//" | sed "s/\\\i0//" > old_bac_names.txt
paste -d,  new_bac_names.txt old_bac_names.txt  | sort  | sed "s/.Candidatus/Candidatus/"  | sed "s/.[}]//" > bac120_r202_name_table.csv
rm old*names.txt
rm new*names.txt