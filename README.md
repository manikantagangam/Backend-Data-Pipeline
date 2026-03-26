# Customer Data Pipeline

## Setup & Run

docker-compose up -d

## Test

curl http://localhost:5000/api/customers?page=1&limit=5
curl -X POST http://localhost:8000/api/ingest
curl http://localhost:8000/api/customers?page=1&limit=5
