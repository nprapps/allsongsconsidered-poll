#!/bin/bash
set -e

csvdedupe $1 --field_names album artist --training_file ./scripts/training.json
