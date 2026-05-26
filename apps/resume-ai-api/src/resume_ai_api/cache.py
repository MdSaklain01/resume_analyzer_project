from __future__ import annotations

import hashlib
import json
from typing import Any

import redis
from redis.exceptions import RedisError

from resume_ai_api.settings import settings


def cache_key(prefix: str, *parts: str) -> str:
    digest = hashlib.sha256("::".join(parts).encode("utf-8")).hexdigest()
    return f"{prefix}:{digest}"


class Cache:
    def __init__(self) -> None:
        self.client: redis.Redis[str] | None = None
        if settings.redis_url:
            self.client = redis.Redis.from_url(settings.redis_url, decode_responses=True)

    def get_json(self, key: str) -> dict[str, Any] | None:
        if not self.client:
            return None
        try:
            value = self.client.get(key)
            return json.loads(value) if value else None
        except RedisError:
            return None

    def set_json(self, key: str, value: dict[str, Any]) -> None:
        if not self.client:
            return
        try:
            self.client.setex(key, settings.cache_ttl_seconds, json.dumps(value))
        except RedisError:
            return


cache = Cache()
