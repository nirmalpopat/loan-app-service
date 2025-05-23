import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.infrastructure.database.base import Base
from app.core.config import settings

# Test database URL
TEST_SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/test_loan_app"

# Create test engine and session
engine = create_async_engine(TEST_SQLALCHEMY_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@pytest.fixture(scope="session")
def test_app():
    client = TestClient(app)
    yield client

@pytest.fixture(scope="function")
async def test_db():
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create a new session for each test
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()
    
    # Drop all tables after test
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
def mock_redis(mocker):
    mock = mocker.MagicMock()
    mocker.patch("app.infrastructure.cache.redis_client.redis_cache", mock)
    return mock

@pytest.fixture
def mock_kafka(mocker):
    mock = mocker.MagicMock()
    mocker.patch("app.infrastructure.messaging.kafka_client.kafka_client", mock)
    return mock
