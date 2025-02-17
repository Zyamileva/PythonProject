import sqlite3


def all_genre():
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
    conn.close()
