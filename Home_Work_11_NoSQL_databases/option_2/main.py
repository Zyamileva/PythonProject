import uuid

import redis
import time

client = redis.Redis(host="localhost", port=6379, decode_responses=True)

print("Connected to Redis...", client.ping())
SESSION_TTL = 1800


def create_session(user_id: str, session_token: str):
    print(f"Creating session for user {user_id}...")
    login_time = int(time.time())
    client.hset(
        f"session:{user_id}",
        mapping={"session_token": session_token, "login_time": login_time},
    )
    client.expire(f"session:{user_id}", SESSION_TTL)


def add_session(user_id: str, session_token: str):
    create_session(user_id, session_token)


def get_session(user_id) -> dict:
    return client.hgetall(f"session:{user_id}")


def update_session_activity(user_id: str):
    print(f"Updating session activity for user {user_id}...")
    client.hset(f"session:{user_id}", "login_time", int(time.time()))
    client.expire(f"session:{user_id}", SESSION_TTL)


def delete_session(user_id):
    print(f"Deleting session for user {user_id}...")
    client.delete(f"session:{user_id}")


if __name__ == "__main__":
    user = "123"
    token = str(uuid.uuid4())
    add_session(user, token)
    print(get_session(user))
    update_session_activity(user)
    print(get_session(user))
    delete_session(user)
    print(get_session(user))
