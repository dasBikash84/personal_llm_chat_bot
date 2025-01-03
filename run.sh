#!/bin/bash

# Ensure the script exits on error
set -e

# Get the port from the command line arguments
PORT=${1:-7860}

# Build the Docker image
docker build -t personal_llm_chat_bot .

# Run the Docker container with specified port
docker run -d --env-file .env -p $PORT:7860 personal_llm_chat_bot