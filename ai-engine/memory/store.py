"""
Long-term Memory Store — Episodic, semantic, and working memory.
Facts are stored with embeddings for semantic recall.
"""

import json
from typing import Optional
import redis.asyncio as aioredis

REDIS_URL = "redis://localhost:6379/0"


class MemoryStore:
    def __init__(self):
        self.redis: Optional[aioredis.Redis] = None

    async def connect(self):
        self.redis = aioredis.from_url(REDIS_URL, decode_responses=True)

    async def store_fact(self, user_id: str, key: str, value: str, importance: float = 0.5):
        memory = {"key": key, "value": value, "importance": importance}
        await self.redis.hset(f"memory:{user_id}", key, json.dumps(memory))
        await self.redis.zadd(f"memory:{user_id}:importance", {key: importance})

    async def recall_fact(self, user_id: str, key: str) -> Optional[str]:
        data = await self.redis.hget(f"memory:{user_id}", key)
        if data:
            return json.loads(data)["value"]
        return None

    async def get_recent_memories(self, user_id: str, limit: int = 10) -> list:
        keys = await self.redis.zrevrange(f"memory:{user_id}:importance", 0, limit - 1)
        memories = []
        for key in keys:
            data = await self.redis.hget(f"memory:{user_id}", key)
            if data:
                memories.append(json.loads(data))
        return memories
