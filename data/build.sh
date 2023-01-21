#! /usr/bin/env bash

# make the appropriate directories
mkdir -p general-analyis/cases_agg general-analysis/temps

mkdir -p state-analysis/cases_agg state-analysis/temps

mkdir -p delhi-analysis/cases_agg delhi-analysis/temps

# unzip the main zip file
unzip csv.zip

# extract judges file
tar xvf judges_clean.tar.gz

# extracting the keys folder
tar xvf keys/keys.tar.gz keys/

# extract acts and sections file
tar xvf acts_sections.tar.gz

# extract cases folder
tar xvf cases/cases.tar.gz cases/
