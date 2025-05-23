import os
from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # App
    APP_ENV: str = "development"
    DEBUG: bool = True
    
    # Database
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    
    # Redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int = 0
    REDIS_TTL: int = 3600  # 1 hour in seconds
    
    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:29092"  # Internal Docker network
    KAFKA_APPLICATION_TOPIC: str = "loan_applications"
    KAFKA_CONSUMER_GROUP_ID: str = "loan_processor"
    KAFKA_AUTO_OFFSET_RESET: str = "earliest"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
