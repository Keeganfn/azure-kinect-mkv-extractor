#!/bin/bash

# The path to the input MKV file and output directory
INPUT_FILE="/path/to/input_file.mkv"
EXTRACTION_FOLDER="/path/to/extraction_folder"

# Set the run options
RUN_OPTIONS="-a"
# RUN_OPTIONS="-p -c -cc"
# RUN_OPTIONS="-p -c -cc --start 3.5 --stop 5.5"
# RUN_OPTIONS="-dcol -cr 0 1500"

# Run the main script with default arguments
./run_in_docker.sh $INPUT_FILE $EXTRACTION_FOLDER $RUN_OPTIONS
