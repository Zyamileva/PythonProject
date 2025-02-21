import sqlite3


def all_genre():
    """Print all unique movie genres.

    Retrieves and displays a comma-separated list of all distinct movie genres present in the database.
    """
    try:
        with sqlite3.connect("my_database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT genre
                FROM movies
            """)
            genrs = cursor.fetchall()
            print("All Genres:")

            mas_genre = []
            mas_genre.extend(genre[0] for genre in genrs)
            print(", ".join(mas_genre))
    except sqlite3.Error as e:
        print(f"Ошибка при подключении к базе данных: {e}")
