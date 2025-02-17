import sqlite3


def list_movies_with_pagination():
    limit = 10
    offset = 0
    while True:
        with sqlite3.connect("my_database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM movies")
            total_movies = cursor.fetchone()[0]
            cursor.execute(
                """
                SELECT title, release_year, genre FROM movies
                LIMIT ? OFFSET ?
            """,
                (limit, offset),
            )
            results = cursor.fetchall()

        count_limit = total_movies - offset if (total_movies - offset) < limit else 10

        if results:
            print(f"\nСтраница {offset // limit + 1} с {count_limit} фильмов:")
            for i, (title, release_year, genre) in enumerate(results, start=1):
                print(f"{i + offset}. {title} ({release_year}), жанр: {genre}")
        else:
            print("Фильмов не найдено.")

        action = input(
            "Введите 'n' для следующей страницы, 'p' для предыдущей или 'q' для выхода: "
        )
        if action == "n":
            offset += limit
        elif action == "p" and offset >= limit:
            offset -= limit
        elif action == "q":
            break
