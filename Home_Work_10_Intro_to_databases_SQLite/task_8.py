import sqlite3
from datetime import datetime


def movie_age(release_year: int) -> int:
    """Calculate the age of a movie.

    Calculates the age of a movie based on its release year.

    Args:
        release_year: The year the movie was released.

    Returns:
        The age of the movie in years.
    """
    current_year = datetime.now().year
    return current_year - release_year


def films_old():
    """Print the age of each movie.

    Retrieves movie titles and their release years from the database, calculates their age using a custom function, and prints the results.
    """
    try:
        with sqlite3.connect("my_database.db") as conn:
            conn.create_function("movie_age", 1, movie_age)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT title, release_year, movie_age(release_year) AS age FROM movies"
            )

            print("Фильмы и их возвраст:")

            for counter, row in enumerate(cursor.fetchall(), start=1):
                print(f'{counter}. Фильм: "{row[0]}" — {row[2]} лет')
    except sqlite3.Error as e:
        print(f"Ошибка при работе с базой данных: {e}")
