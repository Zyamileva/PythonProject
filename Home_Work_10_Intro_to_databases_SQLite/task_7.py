import sqlite3


def name_films_actors():
    """Print all movie titles and actor names.

    Retrieves and displays a combined list of all movie titles and actor names from the database.
    """
    try:
        with sqlite3.connect("my_database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT title AS names FROM movies UNION SELECT name AS names
                              FROM actors""")
            names = cursor.fetchall()
            for counter, name in enumerate(names, start=1):
                print(f"{counter}. {name[0]}")
    except sqlite3.Error as e:
        print(f"Ошибка при работе с базой данных: {e}")