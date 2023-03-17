# namingGTDB

Thousands of new bacterial and archaeal species and higher-level taxa are discovered each year through the analysis of genomes and metagenomes. The Genome Taxonomy Database (GTDB) provides hierarchical sequence-based descriptions and classifications for new and as-yet-unnamed taxa. However, bacterial nomenclature, as currently configured, cannot keep up with the need for new well-formed names. Instead, microbiologists have been forced to use hard-to-remember alphanumeric placeholder labels. Here, we exploit an approach to the generation of well-formed arbitrary Latinate names at a scale sufficient to name tens of thousands of unnamed taxa within GTDB. These newly created names represent an important resource for the microbiology community, facilitating communication between bioinformaticians, microbiologists and taxonomists, while populating the emerging landscape of microbial taxonomic and functional discovery with accessible and memorable linguistic labels.

## Installation

Scripts are written for Python3 (3.7+) and use standard libraries. You can download the repository through github (git clone as below).

```
git clone git@github.com:quadram-institute-bioscience/namingGTDB.git
```

## Usage

rename_GTDB.sh provides a full worked example of running order of all the scripts. rename_GTDB.sh downloads all required input fires (e.g. from GTDB) and runs through all the required steps

## Input files

Input files for this study were obtained from the following sources

- Whitaker's Latin stems: http://archives.nd.edu/whitaker/wordsall.zip
- English Wiktionary headwords: 2021 from https://dumps.wikimedia.org/enwiktionary/20210920/enwiktionary-20210920-pages-articles-multistream-index.txt.bz2
- genus names compiled by Global Biodiversity Information Facility: https://hosted-datasets.gbif.org/datasets/backbone/backbone-current-simple.txt.gz
- GDTB metadata and taxonomy files: https://data.gtdb.ecogenomic.org/releases/release202/202.0/
- ar_genus_endings.txt, bac_genus_endings.txt and species_endings.txt files from https://zenodo.org/deposit/5652886

## Citation

Please cite:

Pallen MJ, Rodriguez-R LM, Alikhan N-F. Naming the unnamed: over 65,000 Candidatus names for unnamed Archaea and Bacteria in the Genome Taxonomy Database. International Journal of Systematic and Evolutionary Microbiology. Microbiology Society; 2022. doi:https://doi.org/10.1099/ijsem.0.005482

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[GPLv3](https://choosealicense.com/licenses/gpl-3.0/)

## CHANGE LOG

**17/03/2023**

An error in the Python scripts used to generate the protologues presented as supplementary material in the paper by Pallen et al (2022) meant that names for the rank of class were not included. Updated scripts have been uploaded that correct this problem and allow generation of protologues for all ranks. See:

- [archaeal_protologue_maker.py](archaeal_protologue_maker.py)
- [bacterial_protologue_maker.py](bacterial_protologue_maker.py)
- [build_protologues_from_named_genera.py](build_protologues_from_named_genera.py)

In addition, we have created [scripts that create protologues only for taxa at the rank of class](classes_only/), which have been used to create additional supplementary files for a corrigendum to the paper that includes new names for classes
