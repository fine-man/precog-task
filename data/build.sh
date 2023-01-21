#! /usr/bin/env bash

# make the appropriate directories
mkdir -p general-analysis/cases_agg general-analysis/temps general-analysis/csv-files

mkdir -p state-analysis/cases_agg state-analysis/temps state-analysis/csv-files

mkdir -p delhi-analysis/cases_agg delhi-analysis/temps delhi-analysis/csv-files

# unzip the main zip file
unzip csv.zip

# extract judges file
tar xvf judges_clean.tar.gz

# extracting the keys folder
tar xvf keys/keys.tar.gz --directory=keys/

# extract acts and sections file
tar xvf acts_sections.tar.gz

# extract cases folder
tar xvf cases/cases.tar.gz --directory=cases/
