import sqlite3
from datetime import datetime


def movie_age(release_year):
    current_year = datetime.now().year
    return current_year - release_year


def films_old():
    with sqlite3.connect("my_database.db") as conn:
        conn.create_function("movie_age", 1, movie_age)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT title, release_year, movie_age(release_year) AS age FROM movies"
        )

        print("Фильмы и их возвраст:")

        for counter, row in enumerate(cursor.fetchall(), start=1):
            print(f'{counter}. Фильм: "{row[0]}" — {row[2]} лет')

        # conn.close()
