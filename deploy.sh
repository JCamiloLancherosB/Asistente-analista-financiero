#!/bin/bash

# Cloud Run deployment script for Financial Assistant

set -e

if [ -z "$1" ]; then
    echo "Usage: ./deploy.sh YOUR_PROJECT_ID"
    exit 1
fi

PROJECT_ID=$1
REGION=${2:-us-central1}
SERVICE_NAME="financial-assistant"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "🚀 Deploying Financial Assistant to Cloud Run"
echo "Project: $PROJECT_ID"
echo "Region: $REGION"
echo ""

# Set project
echo "Setting GCP project..."
gcloud config set project $PROJECT_ID

# Build container
echo "Building container image..."
gcloud builds submit --tag $IMAGE_NAME

# Deploy to Cloud Run
echo "Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image $IMAGE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars PROJECT_ID=$PROJECT_ID \
  --set-env-vars LOCATION=$REGION \
  --set-env-vars GEMINI_MODEL=gemini-1.5-pro \
  --memory 512Mi \
  --cpu 1 \
  --timeout 300

echo ""
echo "✅ Deployment complete!"
echo "Your service is available at:"
gcloud run services describe $SERVICE_NAME --region $REGION --format='value(status.url)'
