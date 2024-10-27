#!/bin/bash

DOCKERFILE_PATH="/home/jostan/Documents/azure-kinect-mkv-extractor/docker/Dockerfile"
BUILD_CONTEXT="/home/jostan/Documents/azure-kinect-mkv-extractor"

docker build -t azure-kinect-mkv-extractor:latest -f "$DOCKERFILE_PATH" "$BUILD_CONTEXT"