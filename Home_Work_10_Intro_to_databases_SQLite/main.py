from Home_Work_10_Intro_to_databases_SQLite.bd import create_tables
from Home_Work_10_Intro_to_databases_SQLite.task_1 import add_movies, add_actors
from Home_Work_10_Intro_to_databases_SQLite.task_2 import all_films_with_actors
from Home_Work_10_Intro_to_databases_SQLite.task_3 import all_genre
from Home_Work_10_Intro_to_databases_SQLite.task_4 import (
    count_film_of_genre,
    avg_year_actor_in_genre,
)
from Home_Work_10_Intro_to_databases_SQLite.task_5 import search_film
from Home_Work_10_Intro_to_databases_SQLite.task_6 import list_movies_with_pagination
from Home_Work_10_Intro_to_databases_SQLite.task_7 import name_films_actors
from Home_Work_10_Intro_to_databases_SQLite.task_8 import films_old


def main():
    create_tables()
    while True:
        print("\nМеню:")
        print("1. Добавить фильм")
        print("2. Добавить актёра")
        print("3. Показать все фильмы с актёрами")
        print("4. Показать все жанры")
        print("5. Показать количество фильмов за жанром")
        print("6. Показать средний год рождения актёров в фильмах определённого жанра")
        print("7. Поиск фильма по названию")
        print("8. Показать фильмы (с пагинацией)")
        print("9. Показать имена всех актёров и названия всех фильмов")
        print("10 Показать список фильмов вместе с их возврастом")
        print("0. Выход")
        choice = input("Выберите опцию: ")
        if choice == "1":
            add_movies()
        elif choice == "2":
            add_actors()
        elif choice == "3":
            all_films_with_actors()
        elif choice == "4":
            all_genre()
        elif choice == "5":
            count_film_of_genre()
        elif choice == "6":
            avg_year_actor_in_genre()
        elif choice == "7":
            search_film()
        elif choice == "8":
            list_movies_with_pagination()
        elif choice == "9":
            name_films_actors()
        elif choice == "10":
            films_old()
        elif choice == "0":
            break
        else:
            print("Неправильный вибор. Попробуйте ещё раз")


if __name__ == "__main__":
    main()
