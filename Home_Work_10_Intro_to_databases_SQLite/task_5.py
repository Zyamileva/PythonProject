import sqlite3


def search_film():
    try:
        with sqlite3.connect("my_database.db") as conn:
            """Search for movies by title.
    
            Prompts the user for a keyword and searches for movies whose titles contain that keyword.
            """
            cursor = conn.cursor()
            title_search = input("Введите ключевое слово для поиска: ")
            cursor.execute(
                """
                SELECT title, release_year
                FROM movies
                WHERE title LIKE ?""",
                (f"%{title_search}%",),
            )
            if response := cursor.fetchall():
                print("Найдены фильмы:")
                for counter, film in enumerate(response, start=1):
                    print(f"{counter}. {film[0]} ({film[1]})")
    except sqlite3.Error as e:
        print(f"Ошибка при работе с базой данных: {e}")
