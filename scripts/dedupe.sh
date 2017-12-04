#!/bin/bash
set -e
OUTPUT_PATH='../output'
mkdir -p $OUTPUT_PATH

echo "Dedupe 2016 entries"
csvdedupe $OUTPUT_PATH'/2016_responses_normalized.csv' --field_names album_artist --output_file $OUTPUT_PATH'/2016_responses_deduped.csv'
