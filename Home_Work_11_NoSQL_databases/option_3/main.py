from cassandra.cluster import Cluster

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


def add_event(event_id, user_id, event_type, metadata):
    timestamp = datetime.now(timezone.utc)
    print(f"adding event {event_id}, {user_id} {event_type} {metadata}")
    session.execute(
        """
        INSERT INTO logs ( event_id, user_id, event_type, timestamp, metadata)
        VALUES (%s, %s, %s, %s, %s)
    """,
        (event_id, user_id, event_type, timestamp, metadata),
    )


def get_recent_events(event_type, user_id):
    since = datetime.now(timezone.utc) - timedelta(days=1)
    return session.execute(
        """
        SELECT * FROM logs WHERE event_type=%s AND user_id=%s AND timestamp >= %s
    """,
        (event_type, user_id, since),
    )


def update_event_metadata(event_type, user_id, event_id, timestamp, metadata):
    session.execute(
        """
        UPDATE logs SET metadata=%s WHERE event_type=%s AND user_id=%s AND event_id=%s AND timestamp=%s
        """,
        (metadata, event_type, user_id, event_id, timestamp),
    )


def delete_old_events(event_type):
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)

    # Получаем старые события
    rows = session.execute(
        """
        SELECT event_id, user_id, timestamp FROM logs WHERE event_type=%s AND timestamp < %s ALLOW FILTERING
        """,
        (event_type, cutoff),
    )

    # Удаляем по event_id
    for row in rows:
        session.execute(
            """
            DELETE FROM logs WHERE event_type=%s AND user_id=%s AND timestamp=%s AND event_id=%s
            """,
            (event_type, row.user_id, row.timestamp, row.event_id),
        )


def delete_all_data():
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
