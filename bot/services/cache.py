
import json
import time
import redis
import logging
from bot.constants import (
    REDIS_HOST, 
    REDIS_PORT, 
    REDIS_PASSWORD,
    REDIS_DATABASE,
    REDIS_CONTEXT_EXPIRED_TIME,
    REDIS_SESSION_EXPIRED_TIME,
)

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

    def save_context(self, user_id, context):
        key = f'user:context:{user_id}'
        self.redis_client.setex(
            key, 
            REDIS_CONTEXT_EXPIRED_TIME*60,  # *60s
            json.dumps(context)
        )

    def get_context(self, user_id):
        key = f'user:context:{user_id}'
        state_data = self.redis_client.get(key)

        if state_data:
            return json.loads(state_data)
        return None

    def clear_context(self, user_id):
        self.redis_client.delete(f'user:context:{user_id}')

    def save_session(self, user_id, session):
        key = f'user:session:{user_id}'
        self.redis_client.setex(
            key, 
            REDIS_SESSION_EXPIRED_TIME*60,  # *60s
            json.dumps(session)
        )

    def get_session(self, user_id):
        key = f'user:session:{user_id}'
        state_data = self.redis_client.get(key)

        if state_data:
            return json.loads(state_data)
        return None

    def clear_session(self, user_id):
        self.redis_client.delete(f'user:session:{user_id}')
