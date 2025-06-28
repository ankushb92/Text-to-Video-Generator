#!/bin/bash

# Root directory where the images folder is located
ROOT_DIR="$(pwd)/deploy/images"

# Function to load and tag Docker images from tarballs
load_image() {
  local tarball_path=$1
  local image_name=$2
  
  echo "Loading Docker image from tarball: $tarball_path"
  
  # Load the tarball into Docker
  docker load -i "$tarball_path" || {
    echo "Failed to load image from $tarball_path"
    return 1
  }

  echo "Successfully loaded image: $image_name"
}

# Iterate over each service directory inside the images folder
for service_dir in "$ROOT_DIR"/*/; do
  # Check if the directory contains a tarball
  if [ -d "$service_dir" ]; then
    for tarball in "$service_dir"/*.tar; do
      if [ -f "$tarball" ]; then
        # Extract service name from the tarball path
        service_name=$(basename "$tarball" .tar)

        # Load the tarball into Docker and tag the image
        load_image "$tarball" "$service_name" || continue
      else
        echo "No tarball found in $service_dir"
      fi
    done
  else
    echo "Skipping $service_dir: Not a directory"
  fi
done


# kubectl rollout restart deployment <deployment-name> to restart deployments
