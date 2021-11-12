# namingGTDB
Thousands of new bacterial and archaeal species and higher-level taxa are discovered each year through the analysis of genomes and metagenomes. The Genome Taxonomy Database (GTDB) provides hierarchical sequence-based descriptions and classifications for new and as-yet-unnamed taxa. However, bacterial nomenclature, as currently configured, cannot keep up with the need for new well-formed names. Instead, microbiologists have been forced to use hard-to-remember alphanumeric placeholder labels. Here, we exploit an approach to the generation of well-formed arbitrary Latinate names at a scale sufficient to name tens of thousands of unnamed taxa within GTDB. These newly created names represent an important resource for the microbiology community, facilitating communication between bioinformaticians, microbiologists and taxonomists, while populating the emerging landscape of microbial taxonomic and functional discovery with accessible and memorable linguistic labels.

## Installation
Scripts are written for Python3 (3.7+) with standard libraries.  You can download the repository through github (git clone as below). 

```
git clone git@github.com:quadram-institute-bioscience/namingGTDB.git
```


## Usage
GTDB_renamer.sh provides a full worked example of running order of all the scripts. GTDB_renamer.sh downloads all required input fires (e.g. from GTDB) and runs through all the required steps 

## Input files
Input files for this study were obtained from the following sources
•	Whitaker's Latin stems: http://archives.nd.edu/whitaker/wordsall.zip 
•	English Wiktionary headwords: 2021 from https://dumps.wikimedia.org/enwiktionary/20210920/enwiktionary-20210920-pages-articles-multistream-index.txt.bz2 
•	genus names compiled by Global Biodiversity Information Facility: https://hosted-datasets.gbif.org/datasets/backbone/backbone-current-simple.txt.gz
•	GDTB metadata and taxonomy files: https://data.gtdb.ecogenomic.org/releases/release202/202.0/
•	ar_genus_endings.txt, bac_genus_endings.txt and species_endings.txt files from https://zenodo.org/deposit/5652886 


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
[GPLv3](https://choosealicense.com/licenses/gpl-3.0/)