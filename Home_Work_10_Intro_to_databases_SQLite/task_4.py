import sqlite3


def count_film_of_genre():
    """Count and print the number of movies for each genre.

    Retrieves the number of movies grouped by genre and displays the results.
    """
    try:
        with sqlite3.connect("my_database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT genre, COUNT(genre)
                FROM movies
                GROUP BY genre
            """)
            count_genre = cursor.fetchall()
            print("Жанры и количество фильмов:")
            for counter, (genre, count) in enumerate(count_genre, start=1):
                print(f"{counter}. {genre}: {count}")
    except sqlite3.Error as e:
        print(f"Ошибка при подключении к базе данных: {e}")


def avg_year_actor_in_genre():
    """Calculate and print the average birth year of actors for each movie genre.

    Retrieves the average birth year of actors grouped by movie genre and displays the results.
    """
    try:
        with sqlite3.connect("my_database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT m.genre as genre, AVG(a.birth_year) as avg_year
                              FROM movies as m
                              INNER JOIN movie_cast as b ON m.id = b.movie_id
                              INNER JOIN actors as a ON b.actor_id = a.id
                              GROUP BY m.genre
                              ORDER BY m.genre""")

            avg_year = cursor.fetchall()
            print("Средний год рождения актёров в жанре:")
            for counter, (genre, year) in enumerate(avg_year, start=1):
                print(
                    f"{counter}. Средний год рождения актёров в жанре: {genre} составляет - {round(year, 2)}"
                )
    except sqlite3.Error as e:
        print(f"Ошибка при подключении к базе данных: {e}")
