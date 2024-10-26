#!/bin/bash

# The path to the input MKV file and output directory
INPUT_FILE="/path/to/input_file.mkv"
EXTRACTION_FOLDER="/path/to/extraction_folder"

# Set the run options
# RUN_OPTIONS="-d -c -s 15 -e 17"
RUN_OPTIONS="-a"

# Run the main script with default arguments
./run_in_docker.sh $INPUT_FILE $EXTRACTION_FOLDER $RUN_OPTIONS
