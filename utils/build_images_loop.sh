#!/bin/bash

TOOL_LIST=$1
SCRIPT_PATH="./build_image.sh"

if [[ -z "${TOOL_LIST}" ]] ; then
    echo "No tool list provided. Exiting..."
    exit 1
else
    while IFS=',' read -r a b; do
        echo "Running: $SCRIPT_PATH $a $b"
        bash "$SCRIPT_PATH" "$a" "$b"
    done < "$TOOL_LIST"
fi
