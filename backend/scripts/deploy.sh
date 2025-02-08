#!/bin/bash

# Deployment script
ENV=$1

if [ "$ENV" != "staging" ] && [ "$ENV" != "production" ]; then
    echo "Invalid environment. Use: staging or production"
    exit 1
fi

echo "Deploying to $ENV..."

# Load environment variables
source .env.$ENV

# Build and push Docker image
docker build -t wolvox-integration:latest .
docker tag wolvox-integration:latest $DOCKER_REGISTRY/wolvox-integration:latest
docker push $DOCKER_REGISTRY/wolvox-integration:latest

# Deploy to server
ssh $DEPLOY_USER@$DEPLOY_HOST "cd /opt/wolvox && \
    docker-compose pull && \
    docker-compose up -d"

echo "Deployment completed!" 