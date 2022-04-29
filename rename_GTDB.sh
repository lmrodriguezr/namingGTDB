## GTDB renamer shell script

##requires associated python scripts to be in the same directory

##enable python scripts to run 
chmod u+x *.py

##download and extract Latin stems from Whitaker's Words
mkdir whitakers_words
wget http://archives.nd.edu/whitaker/old/wordsall.zip
unzip wordsall.zip -d whitakers_words
rm wordsall.zip
mv whitakers_words/STEMLIST.GEN ./
rm -d -r whitakers_words

##download and extract English Wiktionary head words
wget https://dumps.wikimedia.org/enwiktionary/latest/enwiktionary-latest-pages-articles-multistream-index.txt.bz2
bzip2 -d enwiktionary-latest-pages-articles-multistream-index.txt.bz2

##download and extract genus names already in use
wget https://hosted-datasets.gbif.org/datasets/backbone/current/simple.txt.gz

##download and decompress GTDB taxonomy and metadata files; then remove compressed files
wget https://data.gtdb.ecogenomic.org/releases/release207/207.0/ar53_taxonomy_r207.tsv.gz --no-check-certificate
wget https://data.gtdb.ecogenomic.org/releases/release207/207.0/ar53_metadata_r207.tar.gz --no-check-certificate
wget https://data.gtdb.ecogenomic.org/releases/release207/207.0//bac120_taxonomy_r207.tsv.gz --no-check-certificate
wget https://data.gtdb.ecogenomic.org/releases/release207/207.0/bac120_metadata_r207.tar.gz --no-check-certificate
gunzip *.gz
tar -xvzf ar53_metadata_r207.tar
tar -xvzf bac120_metadata_r207.tar
rm *.tar

## extract relevant terms from input files and collate into files of excluded terms
./input_terms_clean.py

## identify and correct anomalies in GTDB taxonomy files; build protologues for new names based on named genera
./anomaly_table_maker.py
./anomalies_clean.py
./build_protologues_from_named_genera.py

##optional step: convert RTF to PDF using Libreoffice; requires Libreoffice to be installed
soffice --headless --convert-to pdf protologues_built_from_named_genera.rtf

##run the scripts to create and curate names and use them to replace alphanumeric placeholders in GTDB files
./genus_stem_creator.py
./name_curator.py --cutoff 2 genus_stems.txt --output_prefix genus_stems
./bac_genus_name_creator.py
./ar_genus_name_creator.py
./species_name_creator.py

./name_table_maker.py -g -t bac120_taxonomy_r207_corrected.tsv -i bac_genus_names.txt 
./name_table_maker.py -g -t ar53_taxonomy_r207_corrected.tsv -i ar_genus_names.txt
./name_table_maker.py -t ar53_taxonomy_r207_corrected.tsv -i species_names.txt 
./name_table_maker.py -t bac120_taxonomy_r207_corrected.tsv -i unused_names_after_creating_ar53_r207_corrected_species_names_table.txt

./taxon_renamer.py -g -t ar53_r207_corrected_ar_genus_names_table.txt  -i ar53_taxonomy_r207_corrected.tsv -o ar53_taxonomy_r207_corrected_gen_renamed_marked.tsv
./taxon_renamer.py -t ar53_r207_corrected_species_names_table.txt  -i ar53_taxonomy_r207_corrected_gen_renamed_marked.tsv -o ar53_taxonomy_r207_corrected_all_renamed_marked.tsv
./taxon_renamer.py -g -t bac120_r207_corrected_bac_genus_names_table.txt  -i bac120_taxonomy_r207_corrected.tsv -o bac120_taxonomy_r207_corrected_gen_renamed_marked.tsv
./taxon_renamer.py -t bac120_r207_corrected_unused_names_after_creating_ar53_r207_corrected_species_names_table_table.txt -i bac120_taxonomy_r207_corrected_gen_renamed_marked.tsv -o bac120_taxonomy_r207_corrected_all_renamed_marked.tsv
cat ar53_taxonomy_r207_corrected_all_renamed_marked.tsv  bac120_taxonomy_r207_corrected_all_renamed_marked.tsv > gtdb_taxonomy_r207_corrected_all_renamed_marked.tsv

##remove markers from taxonomy files
sed 's/[!]//g; s/[|]//g; s/[@]//g' ar53_taxonomy_r207_corrected_all_renamed_marked.tsv > ar53_taxonomy_r207_corrected_all_renamed_unmarked.tsv
sed 's/[!]//g; s/[|]//g; s/[@]//g' bac120_taxonomy_r207_corrected_all_renamed_marked.tsv > bac120_taxonomy_r207_corrected_all_renamed_unmarked.tsv
sed 's/[!]//g; s/[|]//g; s/[@]//g' gtdb_taxonomy_r207_corrected_all_renamed_marked.tsv > gtdb_taxonomy_r207_corrected_all_renamed_unmarked.tsv

##transfer newly named taxonomies into metadata files
./taxa_to_metadata.py -m ar53_metadata_r207.tsv -i ar53_taxonomy_r207_corrected_all_renamed_marked.tsv -o ar53_metadata_r207_renamed.tsv
./taxa_to_metadata.py -m bac120_metadata_r207.tsv -i bac120_taxonomy_r207_corrected_all_renamed_marked.tsv -o bac120_metadata_r207_renamed.tsv

##create the protologues and name tables
./archaeal_protologue_maker.py
./bacterial_protologue_maker.py

##optional step: convert RTF to PDF using Libreoffice; requires Libreoffice to be installed
soffice --headless --convert-to pdf archaeal_protologues.rtf
soffice --headless --convert-to pdf bacterial_protologues.rtf

##create table of all renamed taxa
./all_renamed_taxa_table_maker.py
