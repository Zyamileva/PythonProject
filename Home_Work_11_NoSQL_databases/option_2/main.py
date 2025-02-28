import uuid
import redis
import time

client = redis.Redis(host="localhost", port=6379, decode_responses=True)

print("Connected to Redis...", client.ping())
SESSION_TTL = 1800
SESSION_PREFIX = "session:"


def create_session(user_id: str | int, session_token: str) -> None:
    """Create a new session for a user.

    This function creates a session in Redis for a given user ID and session token, setting the login time and expiry. It performs input validation and handles potential errors during session creation.

    Args:
        user_id (str | int): The ID of the user.
        session_token (str): The unique token for the session.

    Returns:
        None

    Raises:
        ValueError: If user_id or session_token are not strings, or if they are empty.
    """

    if not isinstance(user_id, (str, int)):
        raise ValueError("user_id must be a string")
    user_id = str(user_id)

    if not user_id:
        raise ValueError("user_id cannot be empty")

    if not isinstance(session_token, str):
        raise ValueError("session_token must be a string")

    if not session_token:
        raise ValueError("session_token cannot be empty")

    session_key = "{SESSION_PREFIX}{user_id}"

    print(f"Creating session for user {user_id}...")

    login_time = str(time.time())

    try:
        client.hset(
            session_key,
            mapping={"session_key": session_token, "login_time": login_time},
        )
        client.expire(session_key, SESSION_TTL)
    except Exception as e:
        print(f"Failed to create session for user {user_id}: {str(e)}")


def get_session(user_id: str | int) -> dict:
    """Retrieve a user's session data.

    This function retrieves the session data for the given user ID from Redis.

    Args:
    user_id (str | int): The ID of the user.

    Returns:
    dict: The session data, or an empty dictionary if no session exists.

    Raises:
    ValueError: If user_id is invalid.
    """

    if not user_id:
        raise ValueError("user_id cannot be empty")

    if not isinstance(user_id, (str, int)):
        raise ValueError("user_id must be a string")

    user_id = str(user_id)
    session_key = "{SESSION_PREFIX}{user_id}"

    print(f"Getting session for user {user_id}...")

    try:
        return client.hgetall(session_key) if client.exists(session_key) else {}
    except redis.RedisError as e:
        print(f"Failed to get session for user {user_id}: {e}")
        return {}


def update_session_activity(user_id: str | int) -> bool:
    """Update the activity timestamp of a user's session.

    This function updates the last login time of the user's session in Redis,
    effectively extending the session's lifespan.

    Args:
    user_id (str | int): The ID of the user.

    Returns:
    bool: True if the session was updated successfully, False otherwise.

    Raises:
    ValueError: If user_id is invalid.
    """

    if not user_id:
        raise ValueError("user_id cannot be empty")

    if not isinstance(user_id, (str, int)):
        raise ValueError("user_id must be a string")

    user_id = str(user_id)
    session_key = "{SESSION_PREFIX}{user_id}"

    login_time = str(time.time())

    try:
        if not client.exists(session_key):
            print(f"No session found for user {user_id}.")
            return False
        else:
            client.expire(session_key, SESSION_TTL)
            client.hset(session_key, "login_time", login_time)
            print(f"Session for user {user_id} has been updated.")
            return True
    except redis.RedisError as e:
        print(f"Failed to update session activity for user {user_id}: {e}")
        return False


def delete_session(user_id):
    """Delete a user's session.

    This function deletes the session associated with the given user ID from Redis.

    Args:
    user_id (str | int): The ID of the user.

    Raises:
    ValueError: If user_id is invalid.
    """

    if not user_id:
        raise ValueError("user_id cannot be empty")

    if not isinstance(user_id, (str, int)):
        raise ValueError("user_id must be a string")

    user_id = str(user_id)
    session_key = "{SESSION_PREFIX}{user_id}"

    try:
        if client.exists(session_key):
            print(f"Deleting session for user {user_id}...")
            client.delete(session_key)
        else:
            print(f"No session found for user {user_id}.")
    except redis.RedisError as e:
        print(f"Failed to delete session for user {user_id}: {e}")


if __name__ == "__main__":
    user = "123"
    token = str(uuid.uuid4())
    create_session(user, token)
    print(get_session(user))
    update_session_activity(user)
    time.sleep(5)
    print(get_session(user))
    delete_session(user)
    print(get_session(user))
