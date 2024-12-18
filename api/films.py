from process_database import insert_favorite, get_favorites_by_chat_id, insert_or_update_film_rating, get_film_ratings_by_chat_id

favorites_table = "movie_match/favorites_films"
rating_table = "movie_match/movies_ratings"

def add_film_to_favorites(chat_id, film_id, film_name, film_description):
    insert_favorite(
        tablename=favorites_table,
        chat_id=chat_id,
        film_id=film_id,
        film_name=film_name,
        film_description=film_description
    )

def get_favorites(chat_id):
    return get_favorites_by_chat_id(favorites_table, chat_id)

def set_film_rating(chat_id, film_id, film_name, rating):
    insert_or_update_film_rating(rating_table, chat_id, film_id, film_name, rating)

def get_my_ratings(chat_id):
    return get_film_ratings_by_chat_id(rating_table, chat_id)

