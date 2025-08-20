import redis
import json
import time
from bot.constants import (
    REDIS_HOST, 
    REDIS_PORT, 
    REDIS_PASSWORD,
    REDIS_TIME, 
    REDIS_DATABASE,
    REDIS_STATE_EXPIRED_TIME,
    REDIS_CONTEXT_EXPIRED_TIME,
    REDIS_SESSION_EXPIRED_TIME,
    REDIS_MCP_EXPIRED_TIME
)
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Cache:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=REDIS_HOST, 
            port=REDIS_PORT, 
            password=REDIS_PASSWORD,
            db=REDIS_DATABASE,
            decode_responses=True
        )

    def save_mcp(self, user_id, mcp):
        key = f'user:mcp:{user_id}'
        self.redis_client.setex(
            key, 
            REDIS_MCP_EXPIRED_TIME*60,  # *60s
            json.dumps(mcp)
        )

    def get_mcp(self, user_id):
        key = f'user:mcp:{user_id}'
        state_data = self.redis_client.get(key)

        if state_data:
            return json.loads(state_data)
        return None
    
    def clear_mcp(self, user_id):
        self.redis_client.delete(f'user:mcp:{user_id}')
