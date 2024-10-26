#!/bin/bash

# DOCKERFILE_PATH="/home/jostan/Documents/azure-kinect-mkv-extractor/docker/Dockerfile"
DOCKERFILE_PATH="/home/jostan/OneDrive/Docs/Grad_school/Research/code_projects/azure-kinect-mkv-extractor/docker/Dockerfile"

# BUILD_CONTEXT="/home/jostan/Documents/azure-kinect-mkv-extractor"
BUILD_CONTEXT="/home/jostan/OneDrive/Docs/Grad_school/Research/code_projects/azure-kinect-mkv-extractor"

docker build -t azure_kinect_mkv_extractor:latest -f "$DOCKERFILE_PATH" "$BUILD_CONTEXT"