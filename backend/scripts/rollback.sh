#!/bin/bash

# Environment variables
ENV=${1:-staging}
VERSION=${2}  # Previous version to rollback to

if [ -z "$VERSION" ]; then
    echo "Error: Version parameter is required"
    echo "Usage: ./rollback.sh [environment] [version]"
    exit 1
fi

# Load environment variables
if [ -f ".env.${ENV}" ]; then
    source ".env.${ENV}"
else
    echo "Error: .env.${ENV} file not found"
    exit 1
fi

echo "Rolling back to version ${VERSION}..."

# Pull specific version
docker pull ${DOCKER_REGISTRY}/woocommerce-wolvox:${VERSION}

# Update the image in docker-compose
sed -i "s|image: .*woocommerce-wolvox:.*|image: ${DOCKER_REGISTRY}/woocommerce-wolvox:${VERSION}|g" docker-compose.yml

# Restart the service
docker-compose up -d --no-deps app

# Check if rollback was successful
if [ $? -eq 0 ]; then
    echo "Rollback completed successfully!"
else
    echo "Error: Rollback failed"
    exit 1
fi

# Verify application health
sleep 10  # Wait for service to start

if curl -f "http://localhost:${API_PORT}/health" > /dev/null 2>&1; then
    echo "Application is healthy after rollback"
else
    echo "Error: Application health check failed after rollback"
    echo "Rolling forward to previous version..."
    git checkout docker-compose.yml
    docker-compose up -d --no-deps app
    exit 1
fi 