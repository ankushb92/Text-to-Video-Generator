#!/bin/bash

set -e  # Exit on any error

# Configuration
IMAGES_DIR="$(pwd)/deploy/images"
PROJECT_ROOT="$(pwd)"  # The project root (where api_service is located)

REGISTRY=""  # Set your registry URL (e.g., "docker.io/username" or "gcr.io/project-id")
TAG="latest"  # Default tag, can be overridden

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show usage
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo "  -r, --registry REGISTRY    Docker registry (required)"
    echo "  -t, --tag TAG             Docker image tag (default: latest)"
    echo "  -d, --dir DIRECTORY       Images directory (default: images)"
    echo "  -h, --help               Show this help message"
    echo ""
    echo "Example:"
    echo "  $0 -r docker.io/myuser -t v1.0.0"
    echo "  $0 --registry gcr.io/my-project --tag latest"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -r|--registry)
            REGISTRY="$2"
            shift 2
            ;;
        -t|--tag)
            TAG="$2"
            shift 2
            ;;
        -d|--dir)
            IMAGES_DIR="$2"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

# Validate required parameters
if [[ -z "$REGISTRY" ]]; then
    print_error "Registry is required. Use -r or --registry to specify."
    usage
    exit 1
fi

# Check if images directory exists
if [[ ! -d "$IMAGES_DIR" ]]; then
    print_error "Images directory '$IMAGES_DIR' does not exist."
    exit 1
fi

print_status "Starting build and push process..."
print_status "Registry: $REGISTRY"
print_status "Tag: $TAG"
print_status "Images directory: $IMAGES_DIR"
echo

# Initialize counters
total_services=0
successful_builds=0
failed_builds=0
failed_services=()

# Find all directories with Dockerfile
for service_dir in "$IMAGES_DIR"/*; do
    if [[ -d "$service_dir" ]]; then
        service_name=$(basename "$service_dir")
        dockerfile_path="$service_dir/Dockerfile"
        
        if [[ -f "$dockerfile_path" ]]; then
            total_services=$((total_services + 1))
            image_name="$REGISTRY/$service_name:$TAG"
            
            print_status "Processing service: $service_name"
            echo "  Directory: $service_dir"
            echo "  Image name: $image_name"
            
            # Build the Docker image
            print_status "Building $service_name..."
            if docker build --platform linux/amd64 -t "$image_name" -f "$dockerfile_path" "$PROJECT_ROOT"; then
                print_success "Built $service_name successfully"
                
                # Push the Docker image
                print_status "Pushing $service_name..."
                if docker push "$image_name"; then
                    print_success "Pushed $service_name successfully"
                    successful_builds=$((successful_builds + 1))
                else
                    print_error "Failed to push $service_name"
                    failed_builds=$((failed_builds + 1))
                    failed_services+=("$service_name (push failed)")
                fi
            else
                print_error "Failed to build $service_name"
                failed_builds=$((failed_builds + 1))
                failed_services+=("$service_name (build failed)")
            fi
            
            echo "----------------------------------------"
        else
            print_warning "No Dockerfile found in $service_dir, skipping..."
        fi
    fi
done

# Summary
echo
print_status "Build and push summary:"
echo "  Total services found: $total_services"
echo "  Successful: $successful_builds"
echo "  Failed: $failed_builds"

if [[ $failed_builds -gt 0 ]]; then
    echo
    print_error "Failed services:"
    for service in "${failed_services[@]}"; do
        echo "  - $service"
    done
    exit 1
else
    echo
    print_success "All services built and pushed successfully!"
fi