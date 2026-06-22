import json
from typing import Optional, Any
import redis.asyncio as aioredis
from src.config.settings import settings

redis_client: Optional[aioredis.Redis] = None


async def get_redis() -> aioredis.Redis:
    global redis_client
    if redis_client is None:
        redis_client = aioredis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
        )
    return redis_client


async def cache_get(key: str) -> Optional[str]:
    r = await get_redis()
    return await r.get(key)


async def cache_set(key: str, value: str, expire: int = 300) -> None:
    r = await get_redis()
    await r.set(key, value, ex=expire)


async def cache_delete(key: str) -> None:
    r = await get_redis()
    await r.delete(key)


async def cache_get_json(key: str) -> Optional[Any]:
    data = await cache_get(key)
    return json.loads(data) if data else None


async def cache_set_json(key: str, value: Any, expire: int = 300) -> None:
    await cache_set(key, json.dumps(value), expire)
