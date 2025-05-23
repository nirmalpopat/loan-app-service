Loan Application Processing Service

A microservice for processing loan applications asynchronously using FastAPI, Kafka, PostgreSQL, and Redis.

Features

- Submit loan applications via REST API
- Asynchronous processing using Kafka
- Application status tracking
- Caching with Redis
- Containerized with Docker

Prerequisites

- Docker and Docker Compose
- Python 3.11+

Getting Started

1. Clone the repository
   ```bash
   git clone <repository-url>
   cd loan-application-service
   ```

2. Set up environment variables
   Copy the example environment file and update it if needed:
   ```bash
   cp .env.example .env
   ```

3. Run docker compose
   ```bash
   docker compose up --build
   ```

API Endpoints

Submit a Loan Application
```http
POST /api/v1/applications/
Content-Type: application/json

{
  "applicant_id": "user123",
  "amount": 5000,
  "term_months": 12
}
```

Check Application Status
```http
GET /api/v1/applications/{applicant_id}
```

Development

Setup Development Environment
1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the development server:
   ```bash
   uvicorn main:app --reload
   ```

4. Start the Kafka consumer in a separate terminal:
   ```bash
   python -m scripts.kafka_consumer
   ```

Running Tests
```bash
pytest tests/
```