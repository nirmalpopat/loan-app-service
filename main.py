import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.v1.endpoints import applications
from app.infrastructure.messaging.kafka_client import kafka_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting application...")
    await kafka_client.start()
    yield
    print("Shutting down application...")
    await kafka_client.stop()

app = FastAPI(
    title="Loan Application Service",
    description="API for processing loan applications",
    version="0.1.0",
    lifespan=lifespan
)

# Include API routers
app.include_router(
    applications.router,
    prefix="/api/v1/applications",
    tags=["applications"]
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
