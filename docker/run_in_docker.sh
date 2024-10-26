#!/bin/bash

# Check if the required arguments are passed
if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 <input_file> <extraction_folder> [optional_run_options]"
  exit 1
fi

# Set input and output paths based on passed arguments
LOCAL_INPUT_FILE="$1"
LOCAL_EXTRACTION_FOLDER="$2"

# Ensure the extraction folder exists
if [ ! -d "$LOCAL_EXTRACTION_FOLDER" ]; then
  mkdir -p "$LOCAL_EXTRACTION_FOLDER"
  chown "$(id -u):$(id -g)" "$LOCAL_EXTRACTION_FOLDER"
fi

# Run Docker container with passed parameters
docker run --rm \
    -v "$LOCAL_INPUT_FILE":/home/vscode/azure-kinect-mkv_extractor/input_data/input_data.mkv:ro \
    -v "$LOCAL_EXTRACTION_FOLDER":/home/vscode/azure-kinect-mkv_extractor/extraction_folder:rw \
    -u vscode \
    --network=host \
    azure-kinect-mkv-extractor \
    "${@:3}" /home/vscode/azure-kinect-mkv_extractor/input_data/input_data.mkv /home/vscode/azure-kinect-mkv_extractor/extraction_folder/

