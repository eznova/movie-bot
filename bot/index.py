import os
import re
import json
import requests
from replies import ABOUT_TEAM_REPLY
from helpers import greeting, delete_previous_message, send_text_with_markup, send_picture_with_text, \
                        send_picture_with_reply_markup, handle_session, send_text, gpt_search
from constants import team_path
from my_api_handler import get_recommendation, create_session, connect_session, send_opinion, add_to_favorites, \
                        find_movie_by_description, get_favorites, get_random_movie_by_genre, send_rating, \
                        get_rating
from menu_templates import create_main_menu, create_back_to_menu, create_settings_menu, \
                        create_genre_menu, create_moviecard_menu, create_connect_menu, \
                        create_rate_movie_menu, create_collection_menu

command_function_map = {
    "/start": "greeting",
    "/code": "handle_session",
    "/movie": "gpt_search"
}

def command_dispatcher(message, command_function_map):
    message_text = message['message']['text']
    chat_id = message['message']['chat']['id']
    
    # Перед выполнением команды выводим главное меню
    for command, function_name in command_function_map.items():
        if message_text.startswith(command):
            function_to_call = globals().get(function_name)
            if function_to_call:
                function_to_call(message)
            else:
                send_text(f"Функция {function_name} не найдена", chat_id)
            break
    else:
        send_text("Команда не распознана", chat_id)

def handle_callback(callback_query):
    data = callback_query['data']
    username = callback_query['from']['username']
    chat_id = callback_query['message']['chat']['id']
    message_id = callback_query['message']['message_id']
    
    # Привязка callback_data к функциям-заглушкам
    data_function_map = {
        'match_a_movie': "Поиграем в киношный тиндер!",
        'survey_movie': "Выберите жанр желаемого тайтла",
        'start_survey': "Фильм какого жанра хочешь посмотреть?",
        'choose_mood': "Ты совсем один? Сыграй в бесплатную...",
        'my_collection': "Избранное отборное домашнее",
        'movie_gpt': "Беру нам последний ряд",
        'notification_settings': "Ты кому звОнишь? Тебе",
        'about_team': "Леди баг спешит фиксить",
        'exact_time': "Минут пять десять пятого пять десять пять",
        'frequency': "ЭМОЛЭЙТ ИМПРУВЭД. ВЕРОЯТНОСТЬ ФАЙЕР РЕЗИСТА КРАЙНЕ МАЛА",
        'back_to_menu': None
    }
    
    response_text = data_function_map.get(data)
    
    if data == "back_to_menu":
        delete_previous_message(chat_id, message_id)
        send_text_with_markup("Выберите действие из меню:", chat_id, create_main_menu())
    elif data == 'match_a_movie':
        delete_previous_message(chat_id, message_id)
        send_text_with_markup(response_text, chat_id, create_connect_menu())
    elif data == 'create_session':
        delete_previous_message(chat_id, message_id)
        session_id = create_session(chat_id, username)['session_id']
        send_text_with_markup(
            "Попросите друга ввести код \'{}\' при подключении к сессии. Сессия запустится автоматически".format(session_id), 
            chat_id, 
            create_back_to_menu()
            )
    elif data == 'connect_to_session':
        delete_previous_message(chat_id, message_id)
        send_text(
            """
            Введите команду /code и код сессии, который вам сообщил друг.
            Пример: /code qwertyuiop
            """, 
            chat_id
            )
    elif data.startswith('movie_'):
        text = callback_query['message']['caption']
        opinion = data.split("_")
        film_id = re.search(r'\(id:\s*(\d+)\)', text).group(1)
        session_id = re.search(r'Session ID:\s*(\w+)', text).group(1)
        is_like = True if opinion[1] == "like" else False
        response = send_opinion(chat_id, session_id, film_id, is_like)
        if response["match"] == None:
            send_text_with_markup("Пришлем ответ сразу, как друг выберет", chat_id, create_back_to_menu())
        elif response["match"] == True:
            send_text_with_markup(
                "It's a match! Вы оба лайкнули последний предложенный фильм!", response["chat_id_1"], create_back_to_menu()
                )
            send_text_with_markup(
                "It's a match! Вы оба лайкнули последний предложенный фильм!", response["chat_id_2"], create_back_to_menu()
                )
        elif response["match"] == False:
            movie_info = get_recommendation()
            title, description = movie_info['name'], movie_info['description']
            picture, film_id = movie_info['poster_url'], movie_info['film_id']
            send_picture_with_reply_markup(
                "Предыдущий фильм не подошел. А хотите посмотреть \'{}\' (id: {})? \n {} \n Session ID: {}".format(
                    title, film_id, description, session_id
                    ), 
                response["chat_id_1"], 
                picture, 
                create_tinder_menu()
                )
            send_picture_with_reply_markup(
                "Предыдущий фильм не подошел. А хотите посмотреть \'{}\' (id: {})? \n {} \n Session ID: {}".format(
                    title, film_id, description, session_id
                    ), 
                response["chat_id_2"], 
                picture, 
                create_tinder_menu()
                )
    elif data == 'survey_movie':
        delete_previous_message(chat_id, message_id)
        send_text_with_markup(response_text, chat_id, create_genre_menu())
    elif data.startswith('genre_'):
        requests = {
            "drama": "драма",
            "horror": "хоррор",
            "triller": "триллер",
            "anime": "аниме",
            "comedy": "комедия"
        }
        genre = data.split("_")
        delete_previous_message(chat_id, message_id)
        result = get_random_movie_by_genre(requests[genre[1]])
        title, description = result['name'], result['description']
        picture, film_id = result['poster_url'], result['film_id']
        send_picture_with_reply_markup(
            "Как насчет посмотреть \'{}\' (id: {})? \n {}".format(title, film_id, description), 
            chat_id, 
            picture, 
            create_moviecard_menu()
            )
    elif data == 'another_movie':
        delete_previous_message(chat_id, message_id)
        send_text_with_markup("Скоро сделаем", chat_id, create_genre_menu())
    elif data == 'rate_movie':
        text = callback_query['message']['caption']
        film_name = re.search(r"'([^']+)'", text).group(1)
        film_id = re.search(r'\(id:\s*(\d+)\)', text).group(1)
        send_text_with_markup(
            "Оцени фильм \'{}\' (id: {})".format(film_name, film_id), 
            chat_id, 
            create_rate_movie_menu()
        )
    elif data.startswith("rating_"):
        delete_previous_message(chat_id, message_id)
        text = callback_query['message']['text']
        film_name = re.search(r"'([^']+)'", text).group(1)
        film_id = re.search(r'\(id:\s*(\d+)\)', text).group(1)
        rating = int(data.split("_")[1])
        send_rating(chat_id, film_id, film_name, rating)
        send_text_with_markup("Ваша оценка сохранена в базе!", chat_id, create_main_menu())
    elif data == 'add_to_favorites':
        text = callback_query['message']['caption']
        film_name = re.search(r"'([^']+)'", text).group(1)
        film_id = re.search(r'\(id:\s*(\d+)\)', text).group(1)
        description_match = re.search(r'\?\s*(.+)', text)
        film_description = description_match.group(1) if description_match else None
        add_to_favorites(chat_id, film_id, film_name, film_description)
        send_text_with_markup("Фильм добавлен в избранное! Что дальше?", chat_id, create_main_menu())
    elif data == 'notification_settings':
        delete_previous_message(chat_id, message_id)
        send_text_with_markup(response_text, chat_id, create_settings_menu())
    elif data == 'about_team':
        send_picture_with_text(ABOUT_TEAM_REPLY, chat_id, team_path)
    elif data == 'my_collection':
        delete_previous_message(chat_id, message_id)
        send_text_with_markup("Что хотите посмотреть?", chat_id, create_collection_menu())
    elif data == 'my_ratings':
        rating_list = []
        delete_previous_message(chat_id, message_id)
        rating_raw = get_rating(chat_id)
        if not rating_raw["result"]:
            send_text_with_markup("Отсутствуют записи об оценках", chat_id, create_back_to_menu())
        else:
            for title in rating_raw["result"]:
                line = str(title["film_name"]) + ": " + str(title["rating"])
                rating_list.append(line)
            send_text_with_markup("\n".join(rating_list), chat_id, create_back_to_menu())
    elif data == 'my_favorites':
        favorites_list = []
        result = get_favorites(chat_id)
        if not result["result"]:
            send_text_with_markup("Отсутствуют записи в избранном", chat_id, create_back_to_menu())
        else:
            for title in result["result"]:
                favorites_list.append(title["film_name"])
            send_text_with_markup("\n".join(favorites_list), chat_id, create_back_to_menu())
    elif data == 'gpt_search':
        send_text(
            """
            После команды /movie введите примерное описание того, что хотите посмотреть.
            Например: /movie Аниме о приключениях в другом мире
            """, 
            chat_id
            )
    else:
        delete_previous_message(chat_id, message_id)
        send_text_with_markup(response_text, chat_id, create_back_to_menu())

def handler(event, context):
    if not event:
        return {'statusCode': 200}
    message = json.loads(event['body'])
    print(message)
    
    # Проверка, сообщение или это callback
    if 'message' in message and 'text' in message['message']:
        command_dispatcher(message, command_function_map)
    elif 'callback_query' in message:
        handle_callback(message['callback_query'])

    return {
        'statusCode': 200
    }
