import json

def create_main_menu():
    return json.dumps(
        {
            "inline_keyboard": [
                [{"text": "Выбрать фильм с другом", "callback_data": "match_a_movie"}],
                [{"text": "Что посмотреть?", "callback_data": "survey_movie"}],
                [{"text": "Моя коллекция", "callback_data": "my_collection"}],
                [{"text": "Поиск тайтлов по описанию", "callback_data": "gpt_search"}],
                [{"text": "Настройки уведомлений", "callback_data": "notification_settings"}],
                [{"text": "О команде", "callback_data": "about_team"}],
            ]
        }
    )

def create_settings_menu():
    return json.dumps(
        {
            "inline_keyboard": [
                [{"text": "Выбрать время", "callback_data": "exact_time"}],
                [{"text": "Периодичность", "callback_data": "frequency"}],
                [{"text": "Назад", "callback_data": "back_to_menu"}]
            ]
        }
    )

def create_genre_menu():
    return json.dumps(
        {
            "inline_keyboard": [
                [{"text": "Драма", "callback_data": "genre_drama"}],
                [{"text": "Ужасы", "callback_data": "genre_horror"}],
                [{"text": "Триллеры", "callback_data": "genre_triller"}],
                [{"text": "Аниме", "callback_data": "genre_anime"}],
                [{"text": "Комедии", "callback_data": "genre_comedy"}],
                [{"text": "В главное меню", "callback_data": "back_to_menu"}]
            ]
        }
    )

def create_moviecard_menu():
    return json.dumps(
        {
            "inline_keyboard": [
                [{"text": "Показать другой фильм", "callback_data": "another_movie"}],
                [{"text": "Оценить", "callback_data": "rate_movie"}],
                [{"text": "Добавить в избранное", "callback_data": "add_to_favorites"}],
                [{"text": "В главное меню", "callback_data": "back_to_menu"}]
            ]
        }
    )

def create_rate_movie_menu():
    return json.dumps(
        {
            "inline_keyboard":
                [[{"text": str(rate), "callback_data": f"rating_{rate}"}] for rate in range(0, 11)]
        }
    )

def create_connect_menu():
    return json.dumps(
        {
            "inline_keyboard": [
                [{"text": "Создать сессию", "callback_data": "create_session"}],
                [{"text": "Подключиться к сессии", "callback_data": "connect_to_session"}],
                [{"text": "Назад", "callback_data": "back_to_menu"}]
            ]
        }
    )

def create_collection_menu():
    return json.dumps(
        {
            "inline_keyboard": [
                [{"text": "Мои оценки", "callback_data": "my_ratings"}],
                [{"text": "Избранное", "callback_data": "my_favorites"}],
                [{"text": "Назад", "callback_data": "back_to_menu"}]
            ]
        }
    )

def create_tinder_menu():
    return json.dumps(
        {
            "inline_keyboard": [
                [{"text": "Лайк", "callback_data": "movie_like"}],
                [{"text": "Дизалйк", "callback_data": "movie_dislike"}]
            ]
        }
    )

def create_back_to_menu():
    return json.dumps(
        {
            "inline_keyboard": [
                [{"text": "Вернуться в меню", "callback_data": "back_to_menu"}],
            ]
        }
    )

