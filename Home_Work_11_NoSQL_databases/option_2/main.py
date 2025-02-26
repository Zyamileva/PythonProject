import uuid

import redis
import time

client = redis.Redis(host="localhost", port=6379, decode_responses=True)

print("Connected to Redis...", client.ping())
SESSION_TTL = 1800


def create_session(user_id: str, session_token: str) -> None:
    """Create a new session for a user.

    This function stores session data in Redis, associating a session token and login time with a user ID.  The session is set to expire after a predefined TTL.

    Args:
        user_id (str): The ID of the user.
        session_token (str): The unique token for the session.
    """
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
    """Retrieve a user's session data.

    This function retrieves session information associated with a given user ID from Redis.

    Args:
        user_id: The ID of the user whose session data is to be retrieved.

    Returns:
        dict: A dictionary containing the user's session data.  Returns an empty dictionary if no session data is found.
    """
    return client.hgetall(f"session:{user_id}")


def update_session_activity(user_id: str):
    """Update the last activity time for a user's session.

    This function refreshes the login time of a user's session in Redis, effectively extending the session's lifespan. It also resets the session's expiration timer.

    Args:
        user_id (str): The ID of the user whose session is being updated.
    """
    print(f"Updating session activity for user {user_id}...")
    client.hset(f"session:{user_id}", "login_time", int(time.time()))
    client.expire(f"session:{user_id}", SESSION_TTL)


def delete_session(user_id):
    """Delete a user's session.

    This function removes a user's session data from Redis.

    Args:
        user_id: The ID of the user whose session is to be deleted.
    """
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
