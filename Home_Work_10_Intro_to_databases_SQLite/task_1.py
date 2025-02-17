import sqlite3


def add_movies() -> None:
    """Add a new movie to the database.

    Prompts the user for the movie title, release year, and genre,
    then adds the movie to the database. After adding the movie,
    prompts the user to add actors to the movie.

    Args:
        None

    Returns:
        None

    Raises:
        sqlite3.IntegrityError: If the movie cannot be added to the database.
    """
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
    except sqlite3.IntegrityError as e:
        print(f"Ошибка при добавлении фильма: {e}")


def extracted_from_add_movies(conn, title, release_year, genre) -> int:
    """Insert a new movie into the database.

    Inserts a new movie into the movies table with the given title, release year, and genre.

    Args:
        conn: The database connection.
        title: The title of the movie.
        release_year: The release year of the movie.
        genre: The genre of the movie.

    Returns:
        The ID of the newly inserted movie.
    """
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
    """Add a new actor to the database.

    Prompts the user for the actor's name and birth year, then adds the actor to the database.

    Args:
        None

    Returns:
        None

    Raises:
        sqlite3.IntegrityError: If the actor cannot be added to the database.
    """
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
    except sqlite3.IntegrityError as e:
        print(f"Ошибка при добавлении актера: {e}")


def add_actors_to_movie(film_id: int) -> None:
    """Add actors to a movie.

    Prompts the user for actor names and adds them to the movie's cast in the database.
    The function checks if the actor exists in the database and if they are already in the movie's cast.

    Args:
        film_id: The ID of the movie.

    Returns:
        None

    Raises:
        sqlite3.IntegrityError: If there is an issue adding the actor to the movie cast.
    """
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
    except sqlite3.IntegrityError as e:
        print(f"Ошибка при добавлении актера к фильму: {e}")


def add_actor_to_movie_inner(conn, film_id, actor_id) -> None:
    """Add an actor to a movie's cast.

    Inserts a new record into the movie_cast table, linking an actor to a movie.

    Args:
        conn: The database connection.
        film_id: The ID of the movie.
        actor_id: The ID of the actor.

    Returns:
        None
    """
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
