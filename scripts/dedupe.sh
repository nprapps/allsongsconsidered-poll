#!/bin/bash
set -e
OUTPUT_PATH='../output'
mkdir -p $OUTPUT_PATH

echo "Dedupe 2017 entries"
csvdedupe $OUTPUT_PATH'/2017_responses_normalized.csv' --field_names album artist --output_file $OUTPUT_PATH'/2017_responses_deduped.csv'
