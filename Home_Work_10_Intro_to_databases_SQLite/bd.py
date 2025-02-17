import sqlite3


def create_tables():
    try:
        with sqlite3.connect("my_database.db") as conn:
            connection = conn.cursor()
            connection.execute("PRAGMA foreign_keys=ON")
            connection.execute("""create table  if not exists movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                release_year INTEGER CHECK(release_year > 0),
                genre text NOT NULL
            )""")

            connection.execute("""create table if not exists actors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                birth_year INTEGER CHECK(birth_year > 0)
            )""")

            connection.execute("""create table  if not exists movie_cast (
                movie_id INTEGER NOT NULL,
                actor_id INTEGER NOT NULL,
                PRIMARY KEY(movie_id, actor_id)
                FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE
                FOREIGN KEY (actor_id) REFERENCES actors(id) ON DELETE CASCADE
            )""")
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError as e:
        print(f"ERROR: {e}")
