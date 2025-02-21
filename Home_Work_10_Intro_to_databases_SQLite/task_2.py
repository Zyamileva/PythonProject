import sqlite3


def all_films_with_actors() -> None:
    """Print all movies and their actors.

    Retrieves and displays a list of all movies along with their corresponding actors from the database.
    """
    try:
        with sqlite3.connect("my_database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT m.title AS Фильмы, GROUP_CONCAT(a.name, ', ') AS Актёры
                              FROM movies as m
                              INNER JOIN movie_cast as b ON m.id = b.movie_id
                              INNER JOIN actors as a ON b.actor_id = a.id
                              GROUP BY m.title
                              ORDER BY m.title""")
            rows = cursor.fetchall()
            print("Фильмы и актёры:")
            for counter, row in enumerate(rows, start=1):
                print(f"{counter}. Фильм: {row[0]}, Актёры: {', '.join(row[1].split(','))}")
    except sqlite3.Error as e:
        print(f"Ошибка при подключении к базе данных: {e}")