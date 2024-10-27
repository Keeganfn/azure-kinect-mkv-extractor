#!/bin/bash

# Check if any arguments were passed
if [ $# -eq 0 ]; then
  # No arguments provided; open an interactive shell
  /bin/bash
else
  # Start Xvfb in the background and export DISPLAY. This is done to avoid having to use the -e DiSPLAY=$DISPLAY option in docker run
  Xvfb :99 -screen 0 640x480x24 &  # Start Xvfb
  export DISPLAY=:99                # Set display to :99

  # Run the extract script with the provided arguments
  exec python3 /home/vscode/azure-kinect-mkv-extractor/extract.py "$@"
fi