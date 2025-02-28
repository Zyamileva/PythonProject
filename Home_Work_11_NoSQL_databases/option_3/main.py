from cassandra.cluster import Cluster

from datetime import datetime, timedelta

from cassandra.query import BatchStatement

EVENT_LOG = "event_logs"
LOGS = "logs"
LOGS_TTL = 604800

try:
    cluster = Cluster(["localhost"])
    session = cluster.connect()
    print(session)
    session.set_keyspace(EVENT_LOG)
except Exception as e:
    print(f"Error connecting to Cassandra: {e}")
    exit(1)

session.execute(f"""
    CREATE TABLE IF NOT EXISTS {LOGS} (
    event_id text,
    user_id text,
    event_type TEXT,
    timestamp TIMESTAMP,
    metadata TEXT,
    PRIMARY KEY ((event_type, user_id), timestamp,event_id)
) WITH CLUSTERING ORDER BY (timestamp DESC);
""")


def add_event(event_id: str, user_id: str, event_type: str, metadata: str) -> None:
    """Add an event to the logs table.

    This function inserts a new event into the Cassandra logs table, including a timestamp and metadata. It handles potential errors during insertion.

    Args:
        event_id (str): The unique identifier for the event.
        user_id (str): The ID of the user associated with the event.
        event_type (str): The type of the event.
        metadata (str): Additional information about the event.

    Returns:
        None

    Raises:
        Exception: If there's an error during the database insertion.
    """

    timestamp = datetime.now()

    try:
        session.execute(
            """
            INSERT INTO logs ( event_id, user_id, event_type, timestamp, metadata)
            VALUES (%s, %s, %s, %s, %s)  USING TTL %s
        """,
            (event_id, user_id, event_type, timestamp, metadata, LOGS_TTL),
        )
        print(f"adding event {event_id}, {user_id} {event_type} {metadata}")
    except Exception as er:
        print(f"Error adding event {event_id}, {user_id} {event_type} {metadata}: {er}")


def get_recent_events(event_type: str, user_id: str) -> list:
    """Retrieve recent events of a specific type for a user.

    This function queries the logs table for events of a given type associated with a specific user within the last 24 hours. It handles potential query errors and returns an empty list if any occur.

    Args:
        event_type (str): The type of event to retrieve.
        user_id (str): The ID of the user for whom to retrieve events.

    Returns:
        list: A list of events matching the criteria, or an empty list if an error occurs.
    """

    since = datetime.now() - timedelta(days=1)
    try:
        return session.execute(
            f"""
            SELECT * FROM {LOGS} WHERE event_type=%s AND user_id=%s AND timestamp >= %s
        """,
            (event_type, user_id, since),
        )
    except Exception as er:
        print(f"Error retrieving recent events for {event_type} {user_id}: {er}")
        return []


def update_event_metadata(
    event_type: str, user_id: str, event_id: str, timestamp: datetime, metadata: str
) -> None:
    """Update the metadata of a specific event.

    This function updates the metadata of an existing event in the logs table, identified by its event type, user ID, event ID, and timestamp. It first checks if the event exists before attempting the update.

    Args:
        event_type (str): The type of the event.
        user_id (str): The ID of the user associated with the event.
        event_id (str): The unique identifier for the event.
        timestamp (datetime): The timestamp of the event.
        metadata (str): The new metadata for the event.

    Returns:
        None
    """
    try:
        if session.execute(
            """
            SELECT event_id FROM logs 
            WHERE event_type=%s AND user_id=%s AND event_id=%s AND timestamp=%s
            """,
            (event_type, user_id, event_id, timestamp),
        ).one():
            session.execute(
                """
                UPDATE logs SET metadata=%s WHERE event_type=%s AND user_id=%s AND event_id=%s AND timestamp=%s
                """,
                (metadata, event_type, user_id, event_id, timestamp),
            )
            print(f"Updated metadata for {event_type} {user_id} {event_id} {timestamp}")
        else:
            print(f"Event {event_id} not found, metadata not updated.")
    except Exception as er:
        print(
            f"Error updating metadata for {event_type} {user_id} {event_id} {timestamp}: {er}"
        )


def delete_old_events(event_type: str) -> None:
    """Delete events older than seven days for a given event type.

    This function removes events of a specified type from the logs table if they are older than a week. It uses a batch statement for efficient deletion.

    Args:
        event_type (str): The type of event to delete.

    Returns:
        None
    """
    cutoff = datetime.now() - timedelta(days=7)
    try:
        rows = session.execute(
            """
            SELECT event_id, user_id, timestamp FROM logs 
            WHERE event_type=%s AND timestamp < %s
            """,
            (event_type, cutoff),
        )

        batch = BatchStatement()

        for row_del in rows:
            batch.add(
                """
                DELETE FROM logs WHERE event_type=%s AND user_id=%s AND timestamp=%s AND event_id=%s
                """,
                (event_type, row_del.user_id, row_del.timestamp, row_del.event_id),
            )

        if len(batch) > 0:
            session.execute(batch)
            print("Old events deleted!")
    except Exception as ex:
        print(f"Error deleting old events for type: {ex}", event_type)


def delete_all_data():
    """Delete the logs table.

    This function attempts to drop the "logs" table if it exists. It handles potential errors during the table deletion process.

    Args:
        None

    Returns:
        None
    """
    try:
        session.execute("DROP TABLE IF EXISTS logs")
        print("Dropping logs")
    except Exception as ex:
        print(f"Error deleting logs table {ex}")


if __name__ == "__main__":
    user = "4"
    event = "4"
    event_type_user = "LOGIN"
    metadata_user = "Logged in"

    add_event(event, user, event_type_user, metadata_user)
    print(f"Event added for user {user}")

    print("Events:")
    for row in get_recent_events(event_type_user, user):
        print(row)

    new_metadata_user = "User logged in successfully"

    for row in get_recent_events(event_type_user, user):
        update_event_metadata(
            event_type_user, user, event, row.timestamp, new_metadata_user
        )

    print("Metadata updated!")

    print("Updated events:")
    for row in get_recent_events(event_type_user, user):
        print(row)

    delete_old_events(event_type_user)
    print("Old events deleted!")
