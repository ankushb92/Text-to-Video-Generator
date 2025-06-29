#!/bin/bash

# Root directory where the images folder is located
ROOT_DIR="$(pwd)/deploy/images"
PROJECT_ROOT="$(pwd)"  # The project root (where api_service is located)

# Iterate over each service directory inside the images folder
for service_dir in "$ROOT_DIR"/*/; do
  # Check if it's a directory and contains a Dockerfile
  if [ -d "$service_dir" ] && [ -f "$service_dir/Dockerfile" ]; then
    # Extract the service name from the directory path
    service_name=$(basename "$service_dir")
    
    echo "Building Docker image for service: $service_name"

    # Set the build context to the root project directory
    build_context="$PROJECT_ROOT"  # This will include api_service

    # Build the Docker image and tag it with the service name
    docker build --platform linux/amd64 -t "$service_name" -f "$service_dir/Dockerfile" "$build_context" || {
      echo "Failed to build Docker image for $service_name"
      continue
    }

    # Save the image as a tarball in the service directory
    docker save -o "$service_dir/$service_name.tar" "$service_name" || {
      echo "Failed to save Docker image for $service_name"
      continue
    }

    echo "Docker image for $service_name saved as $service_name.tar"
  else
    echo "Skipping $service_dir: No Dockerfile found"
  fi
done
