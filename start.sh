#!/bin/bash
set -e

echo "Starting CloudOps Monitor..."

docker compose up --build -d

echo "Waiting for services..."
sleep 10

echo "Frontend:   http://localhost:8501"
echo "Backend:    http://localhost:8001/docs"
echo "Prometheus: http://localhost:9090"
echo "Grafana:    http://localhost:3000"
echo "Grafana login: admin / admin"
