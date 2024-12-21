from process_database import insert_favorite, get_favorites_by_chat_id, insert_or_update_film_rating, get_film_ratings_by_chat_id

favorites_table = "movie_match/favorites_films"  # Таблица для хранения избранных фильмов
rating_table = "movie_match/movies_ratings"  # Таблица для хранения рейтингов фильмов

def add_film_to_favorites(chat_id, film_id, film_name, film_description):
    """
    Добавляет фильм в список избранного для заданного пользователя (чат).
    
    :param chat_id: Идентификатор чата (пользователя)
    :param film_id: Уникальный идентификатор фильма
    :param film_name: Название фильма
    :param film_description: Описание фильма
    """
    insert_favorite(
        tablename=favorites_table,
        chat_id=chat_id,
        film_id=film_id,
        film_name=film_name,
        film_description=film_description
    )

def get_favorites(chat_id):
    """
    Получает список избранных фильмов для заданного пользователя (чата).
    
    :param chat_id: Идентификатор чата (пользователя)
    :return: Список избранных фильмов
    """
    return get_favorites_by_chat_id(favorites_table, chat_id)

def set_film_rating(chat_id, film_id, film_name, rating):
    """
    Устанавливает или обновляет рейтинг фильма для заданного пользователя (чата).
    
    :param chat_id: Идентификатор чата (пользователя)
    :param film_id: Уникальный идентификатор фильма
    :param film_name: Название фильма
    :param rating: Оценка фильма (например, от 1 до 5)
    """
    insert_or_update_film_rating(rating_table, chat_id, film_id, film_name, rating)

def get_my_ratings(chat_id):
    """
    Получает список всех фильмов с их оценками для заданного пользователя (чата).
    
    :param chat_id: Идентификатор чата (пользователя)
    :return: Список фильмов с оценками
    """
    return get_film_ratings_by_chat_id(rating_table, chat_id)
