#!/bin/bash

TOOL=$1
VERSION=$2
CHANNELS='-c bioconda -c conda-forge'
AGGREGATED_PATH='mamba_search_results.tsv'

RESULT=$(mamba search ${CHANNELS} ${TOOL}=${VERSION} | tail -1)
echo $RESULT

if [[ ! -z "${RESULT}" ]]; then
    echo $RESULT >> $AGGREGATED_PATH
fi
