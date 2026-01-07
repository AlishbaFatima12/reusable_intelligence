#!/bin/bash
# Deploy LearnFlow to local Minikube

set -e

echo "🚀 Deploying LearnFlow to Minikube..."

# Check Minikube is running
if ! minikube status &> /dev/null; then
  echo "❌ Minikube is not running. Start it with: minikube start"
  exit 1
fi

# Create namespace
kubectl create namespace learnflow --dry-run=client -o yaml | kubectl apply -f -

# Apply Dapr components
kubectl apply -f ../dapr/components/ -n learnflow

# Apply Kubernetes manifests
kubectl apply -f ../kubernetes/ -n learnflow

echo "✅ Deployment complete!"
echo "📊 Check status: kubectl get pods -n learnflow"
