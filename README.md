# Customer Data Pipeline

## Setup & Run

docker-compose up -d

## Test

curl http://localhost:5000/api/customers?page=1&limit=5
curl -X POST http://localhost:8000/api/ingest
curl http://localhost:8000/api/customers?page=1&limit=5

# Build and start all 3 services

docker-compose up -d --build

# Check all containers are running

docker-compose ps

# Test Flask mock server

curl http://localhost:5000/api/health
curl "http://localhost:5000/api/customers?page=1&limit=5"
curl http://localhost:5000/api/customers/C001

# Trigger ingestion into PostgreSQL

curl -X POST http://localhost:8000/api/ingest

# Query customers from database via FastAPI

curl "http://localhost:8000/api/customers?page=1&limit=5"
curl http://localhost:8000/api/customers/C001

# View logs if something fails

docker-compose logs mock-server
docker-compose logs pipeline-service
