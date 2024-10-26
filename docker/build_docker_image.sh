#!/bin/bash

DOCKERFILE_PATH="/home/jostan/Documents/azure-kinect-mkv-extractor/docker/Dockerfile"
BUILD_CONTEXT="/home/jostan/Documents/azure-kinect-mkv-extractor"

docker build -t azure_kinect_mkv_extractor:latest -f "$DOCKERFILE_PATH" "$BUILD_CONTEXT"