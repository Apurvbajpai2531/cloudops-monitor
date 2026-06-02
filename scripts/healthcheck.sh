#!/bin/bash
set -e

echo "Checking backend..."
curl -f http://localhost:8000/health

echo ""
echo "Checking frontend..."
curl -f http://localhost:8501

echo ""
echo "Checking Prometheus..."
curl -f http://localhost:9090

echo ""
echo "All services are healthy"
