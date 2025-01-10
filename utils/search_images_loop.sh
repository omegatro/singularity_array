#!/bin/bash

TOOL_LIST=$1

SCRIPT_PATH="./search_image_mamba.sh"
AGGREGATED_PATH='mamba_search_results.tsv'

[ -f "${AGGREGATED_PATH}" ] && rm "${AGGREGATED_PATH}"

cat $TOOL_LIST | while IFS=',' read -r a b; do $SCRIPT_PATH $a $b; done
