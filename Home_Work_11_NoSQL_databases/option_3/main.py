from cassandra.cluster import Cluster, ResultSet

from datetime import datetime, timedelta, timezone

cluster = Cluster(["localhost"])
session = cluster.connect()
print(session)
session.set_keyspace("event_logs")

session.execute("""
    CREATE TABLE IF NOT EXISTS logs (
    event_id text,
    user_id text,
    event_type TEXT,
    timestamp TIMESTAMP,
    metadata TEXT,
    PRIMARY KEY ((event_type, user_id), timestamp,event_id)
) WITH CLUSTERING ORDER BY (timestamp DESC);
""")


def add_event(event_id:str, user_id:str, event_type:str, metadata:str)->None:
    """Add an event to the logs table.

    This function inserts a new event record into the Cassandra "logs" table with the provided event details and a UTC timestamp.

    Args:
        event_id: The unique identifier for the event.
        user_id: The ID of the user associated with the event.
        event_type: The type of the event.
        metadata: Additional information about the event.
    """
    timestamp = datetime.now(timezone.utc)
    print(f"adding event {event_id}, {user_id} {event_type} {metadata}")
    session.execute(
        """
        INSERT INTO logs ( event_id, user_id, event_type, timestamp, metadata)
        VALUES (%s, %s, %s, %s, %s)
    """,
        (event_id, user_id, event_type, timestamp, metadata),
    )


def get_recent_events(event_type:str, user_id:str)->ResultSet:
    """Retrieve recent events of a specific type for a user.

    This function queries the Cassandra "logs" table for events matching the given type and user ID that occurred within the last 24 hours.

    Args:
        event_type: The type of event to retrieve.
        user_id: The ID of the user whose events are to be retrieved.

    Returns:
        cassandra.cluster.ResultSet: A result set containing the matching events.
    """
    since = datetime.now(timezone.utc) - timedelta(days=1)
    return session.execute(
        """
        SELECT * FROM logs WHERE event_type=%s AND user_id=%s AND timestamp >= %s
    """,
        (event_type, user_id, since),
    )


def update_event_metadata(event_type:str, user_id:str, event_id:str, timestamp:timezone, metadata:str)->None:
    """Update the metadata of a specific event in the logs table.

    This function updates the metadata of an existing event in the Cassandra "logs" table based on the provided event type, user ID, event ID, and timestamp.

    Args:
        event_type (str): The type of the event.
        user_id (str): The ID of the user associated with the event.
        event_id (str): The unique identifier for the event.
        timestamp (timezone): The timestamp of the event.
        metadata (str): The new metadata for the event.
    """
    session.execute(
        """
        UPDATE logs SET metadata=%s WHERE event_type=%s AND user_id=%s AND event_id=%s AND timestamp=%s
        """,
        (metadata, event_type, user_id, event_id, timestamp),
    )


def delete_old_events(event_type:str)->None:
    """Delete events older than 7 days for a given event type.

    This function removes events from the Cassandra "logs" table that are older than a week for a specified event type.  It retrieves the events to be deleted and then deletes them individually to avoid performance issues with large IN queries.

    Args:
        event_type (str): The type of event to delete old entries for.
    """
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)

    rows = session.execute(
        """
        SELECT event_id, user_id, timestamp FROM logs WHERE event_type=%s AND timestamp < %s ALLOW FILTERING
        """,
        (event_type, cutoff),
    )

    for row in rows:
        session.execute(
            """
            DELETE FROM logs WHERE event_type=%s AND user_id=%s AND timestamp=%s AND event_id=%s
            """,
            (event_type, row.user_id, row.timestamp, row.event_id),
        )


def delete_all_data():
    """Delete the "logs" table.

    This function drops the "logs" table from the Cassandra database if it exists.
    """
    session.execute("DROP TABLE IF EXISTS logs")
    print("Таблица logs удалена!")


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
