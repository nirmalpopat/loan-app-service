import redis.asyncio as redis
from typing import Optional, Any, Dict
import json
from datetime import timedelta
from app.core.config import settings

class RedisCache:
    def __init__(self):
        self.redis = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )
    
    async def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Get a value from Redis cache"""
        value = await self.redis.get(key)
        if value is None:
            return None
        return json.loads(value)
    
    async def set(
        self, 
        key: str, 
        value: Dict[str, Any], 
        expire: Optional[int] = None
    ) -> None:
        """Set a value in Redis cache with optional expiration"""
        if expire is None:
            expire = settings.REDIS_TTL
        
        await self.redis.set(
            key,
            json.dumps(value, default=str),
            ex=expire
        )
    
    async def delete(self, key: str) -> None:
        """Delete a key from Redis cache"""
        await self.redis.delete(key)
    
    async def close(self) -> None:
        """Close the Redis connection"""
        await self.redis.close()

redis_cache = RedisCache()
