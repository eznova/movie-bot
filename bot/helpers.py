import requests
from replies import GREETING_REPLY
from constants import POPCORNENOK_PATH, URL
from menu_templates import create_main_menu, create_tinder_menu, create_back_to_menu
from my_api_handler import connect_session, get_recommendation, find_movie_by_description

def send_text(reply, chat_id):
    url = URL + "sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": reply
    }
    requests.post(url, json=payload)

def edit_message_with_markup(reply, chat_id, message_id, reply_markup=None):
    url = URL + "editMessageText"
    payload = {
        "chat_id": chat_id,
        "text": reply,
        "message_id": message_id,
        "reply_markup": reply_markup
    }
    requests.post(url, json=payload)

def send_text_with_markup(reply, chat_id, reply_markup=None):
    url = URL + "sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": reply,
        "reply_markup": reply_markup
    }
    requests.post(url, json=payload)

def send_picture_with_text(text, chat_id, pic_id):
    url = URL + "sendPhoto"
    data = {
        'photo': pic_id,
        'chat_id': chat_id,
        'caption': text
    }
    requests.post(url, data=data)

def send_picture_with_reply_markup(text, chat_id, pic_id, reply_markup=None):
    url = URL + "sendPhoto"
    data = {
        'photo': pic_id,
        'chat_id': chat_id,
        'caption': text,
        "reply_markup": reply_markup
    }
    requests.post(url, data=data)

def delete_previous_message(chat_id, message_id):
    requests.get(URL + f"deleteMessage?chat_id={chat_id}&message_id={message_id}")

def greeting(message):
    chat_id = message['message']['chat']['id']
    username = message['message']['from']['username']
    send_picture_with_text(GREETING_REPLY.format(username), chat_id, POPCORNENOK_PATH)
    send_text_with_markup("Выберите команду:", chat_id, create_main_menu())

def handle_session(message):
    chat_id = message['message']['chat']['id']
    username = message['message']['from']['username']
    text = message['message']['text']
    command = text.split(" ")
    if len(command) <= 1:
        send_text("Неправильный формат ввода кода. Попробуйте еще раз", chat_id)
    else:
        connection_answer = connect_session(chat_id, username, command[1])
        if str(connection_answer["friend_name"]) != 'null':
            send_text(
                "Вы подключились к сессии с {}!".format(connection_answer["friend_name"]), 
                chat_id
                )
            movie_info = get_recommendation()
            title, description = movie_info['name'], movie_info['description']
            picture, film_id = movie_info['poster_url'], movie_info['film_id']
            send_picture_with_reply_markup(
                "Хотите ли вы посмотреть фильм \'{}\' (id: {}) с {}? \n {} \n Session ID: {}".format(
                    title, film_id, connection_answer["friend_name"], description, command[1]
                    ), 
                chat_id, 
                picture, 
                create_tinder_menu()
                )
            send_picture_with_reply_markup(
                "Хотите ли вы посмотреть фильм \'{}\' (id: {}) с {}? \n {} \n Session ID: {}".format(
                    title, film_id, username, description, command[1]
                    ), 
                connection_answer["friend_id"], 
                picture, 
                create_tinder_menu()
                )
        else: 
            send_text_with_markup("Такой сессии не существует. Выберите команду:", chat_id, create_main_menu())

def gpt_search(message):
    chat_id = message['message']['chat']['id']
    username = message['message']['from']['username']
    text = message['message']['text']
    command = text.split(" ")
    if len(command) <= 1:
        send_text("Неправильный формат ввода кода. Попробуйте еще раз", chat_id)
    else:
        user_input = " ".join(command[1:])
        response = find_movie_by_description(user_input)
        send_text_with_markup(response["result"], chat_id, create_back_to_menu())

