import sqlite3


def add_movies() -> None:
    while True:
        title = input("Введите название фильма:")
        if title == "":
            print("Описание не может быть пустым. Введите описание фильма повторно:")
            continue
        break

    while True:
        release_year = input("Введите год выпуска фильма:")
        if not release_year.isdigit():
            print("Год выпуска должен быть целым числом.")
            continue
        break

    while True:
        genre = input("Введите жанр фильма:")
        if genre == "":
            print("Жанр не может быть пустым. Введите жанр фильма повторно:")
            continue
        break

    try:
        with sqlite3.connect("my_database.db") as conn:
            film_id = extracted_from_add_movies(conn, title, release_year, genre)
            add_actors_to_movie(film_id)
        conn.close()
    except sqlite3.IntegrityError as e:
        print(f"Ошибка при добавлении фильма: {e}")


def extracted_from_add_movies(conn, title, release_year, genre) -> int:
    cursor = conn.cursor()
    cursor.execute(
        """ INSERT INTO movies (title, release_year, genre)
                VALUES (?, ?, ?)""",
        (title, release_year, genre),
    )
    film_id = cursor.lastrowid
    conn.commit()
    print("Фильм успешно добавлен!")
    return film_id


def add_actors():
    while True:
        name = input("Введите имя актера:")
        if name == "":
            print("Имя актера не может быть пустым. Введите имя актера повторно:")
            continue
        break

    while True:
        birth_year = input("Введите год рождения актера:")
        if not birth_year.isdigit():
            print("Год рождения должен быть целым числом.")
            continue
        break

    try:
        with sqlite3.connect("my_database.db") as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO actors (name, birth_year)
                VALUES (?, ?)
            """,
                (name, birth_year),
            )

            conn.commit()
            print("Актер успешно добавлен!")
        conn.close()
    except sqlite3.IntegrityError as e:
        print(f"Ошибка при добавлении актера: {e}")


def add_actors_to_movie(film_id: int) -> None:
    try:
        with sqlite3.connect("my_database.db") as conn:
            cursor = conn.cursor()
            while True:
                name_actor = input("Введите имя актера или оставьте поле пустым:")
                if not name_actor:
                    break
                cursor.execute(
                    """
                    SELECT id FROM actors WHERE name =?
                """,
                    (name_actor,),
                )
                actor_id = cursor.fetchone()
                if not actor_id:
                    print("Актер с таким именем не найден!")
                    continue
                else:
                    actor_id = actor_id[0]
                cursor.execute(
                    """
                    SELECT COUNT(*) FROM movie_cast WHERE movie_id =? AND actor_id =?
                """,
                    (film_id, actor_id),
                )
                if cursor.fetchone()[0] > 0:
                    print("Актер уже добавлен к этому фильму!")
                else:
                    add_actor_to_movie_inner(conn, film_id, actor_id)
        conn.close()
    except sqlite3.IntegrityError as e:
        print(f"Ошибка при добавлении актера к фильму: {e}")


def add_actor_to_movie_inner(conn, film_id, actor_id) -> None:
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO movie_cast (movie_id, actor_id)
        VALUES (?, ?)
    """,
        (film_id, actor_id),
    )

    conn.commit()
    print("Актер добавлен к фильму!")
