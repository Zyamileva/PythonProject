import sqlite3


def name_films_actors():
    with sqlite3.connect("my_database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT title AS names FROM movies UNION SELECT name AS names
                          FROM actors""")
        names = cursor.fetchall()
        for counter, name in enumerate(names, start=1):
            print(f"{counter}. {name[0]}")
