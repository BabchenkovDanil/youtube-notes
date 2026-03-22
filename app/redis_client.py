import redis
import json
from typing import Optional

redis_client = redis.Redis('localhost', port=6379, decode_responses=True)
SESSION_TTL = 30 * 60

def save_session(user_id: int, user_data: dict):
    key = f'session:{user_id}'
    redis_client.setex(key, SESSION_TTL, json.dumps(user_data))

def get_session(user_id: int,) -> Optional[dict]:
    key = f'session{user_id}'
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None

def delete_session(user_id: int):
    key = f'session{user_id}'
    redis_client.delete(key)

def refresh_session(user_id: int):
    key = f'session{user_id}'
    redis_client.expire(key, SESSION_TTL)