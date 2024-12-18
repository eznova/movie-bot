import json
import requests

def get_recommendation():
    url = "https://d5d30qf1gfnohkmkl679.apigw.yandexcloud.net/get_recommendation"
    headers = {
        "X-Request-Path": "get_recommendation",
        "Content-Type": "application/json"
    }
    data = {}
    response = requests.get(url, headers=headers, json=data, timeout=30)
    print("Ответ: {}".format(response))
    
    if response.status_code == 200:
        response_dict = response.json()
        print("Успешный ответ:", response_dict)
        return response_dict
    else:
        print("Ошибка:", response.status_code, response.text)

def create_session(chat_id, username):
    url = "https://d5d30qf1gfnohkmkl679.apigw.yandexcloud.net/create_session"
    headers = {
        "X-Request-Path": "create_session",
        "Content-Type": "application/json"
    }
    data = {"chat_id": chat_id, "user_name": username}
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        response_dict = response.json()
        print("Успешный ответ:", response_dict)
        return response_dict
    else:
        print("Ошибка:", response.status_code, response.text)

def connect_session(chat_id, username, session_id):
    url = "https://d5d30qf1gfnohkmkl679.apigw.yandexcloud.net/approve_session"
    headers = {
        "X-Request-Path": "approve_session",
        "Content-Type": "application/json"
    }
    data = {"chat_id": chat_id, "user_name": username, "session_id": session_id}
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        response_dict = response.json()
        print("Успешный ответ:", response_dict)
        return response_dict
    else:
        print("Ошибка:", response.status_code, response.text)

def send_opinion(chat_id, session_id, film_id, opinion):
    url = "https://d5d30qf1gfnohkmkl679.apigw.yandexcloud.net/send_recommendation_opinion"
    headers = {
        "X-Request-Path": "send_recommendation_opinion",
        "Content-Type": "application/json"
    }
    data = {"chat_id": chat_id, "session_id": session_id, "film_id": film_id, "opinion": "{}".format(opinion)}
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        response_dict = response.json()
        print("Успешный ответ:", response_dict)
        return response_dict
    else:
        print("Ошибка:", response.status_code, response.text)

def add_to_favorites(chat_id, film_id, film_name, film_description):
    url = "https://d5d30qf1gfnohkmkl679.apigw.yandexcloud.net/add_favorite"
    headers = {
        "X-Request-Path": "add_favorite",
        "Content-Type": "application/json"
    }
    data = {
        "chat_id": chat_id, 
        "film_id": film_id, 
        "film_name": film_name, 
        "film_description": film_description
        }
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print("Успешный ответ:", response.status_code)
    else:
        print("Ошибка:", response.status_code, response.text)

def find_movie_by_description(description):
    url = "https://d5d30qf1gfnohkmkl679.apigw.yandexcloud.net/get_movies_by_description"
    headers = {
        "X-Request-Path": "get_movies_by_description",
        "Content-Type": "application/json"
    }
    data = {"description": description}
    response = requests.get(url, headers=headers, json=data)
    
    if response.status_code == 200:
        response_dict = response.json()
        print("Успешный ответ:", response_dict)
        return response_dict
    else:
        print("Ошибка:", response.status_code, response.text)

def get_favorites(chat_id):
    url = "https://d5d30qf1gfnohkmkl679.apigw.yandexcloud.net/get_favorites"
    headers = {
        "X-Request-Path": "get_favorites",
        "Content-Type": "application/json"
    }
    data = {"chat_id": "{}".format(chat_id)}
    response = requests.get(url, headers=headers, json=data)
    
    if response.status_code == 200:
        response_dict = response.json()
        print("Успешный ответ:", response_dict)
        return response_dict
    else:
        print("Ошибка:", response.status_code, response.text)

def get_random_movie_by_genre(genre):
    url = "https://d5d30qf1gfnohkmkl679.apigw.yandexcloud.net/get_random_movie_by_genre"
    headers = {
        "X-Request-Path": "get_random_movie_by_genre",
        "Content-Type": "application/json"
    }
    data = {"genre": genre}
    response = requests.get(url, headers=headers, json=data)
    
    if response.status_code == 200:
        response_dict = response.json()
        print("Успешный ответ:", response_dict)
        return response_dict
    else:
        print("Ошибка:", response.status_code, response.text)

def send_rating(chat_id, film_id, film_name, rating):
    url = "https://d5d30qf1gfnohkmkl679.apigw.yandexcloud.net/send_rating"
    headers = {
        "X-Request-Path": "send_rating",
        "Content-Type": "application/json"
    }
    data = {"chat_id": str(chat_id), "film_id": str(film_id), "film_name": str(film_name), "rating": rating}
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print("Успешный ответ:", response.status_code)
    else:
        print("Ошибка:", response.status_code, response.text)

def get_rating(chat_id):
    url = "https://d5d30qf1gfnohkmkl679.apigw.yandexcloud.net/get_rating"
    headers = {
        "X-Request-Path": "get_rating",
        "Content-Type": "application/json"
    }
    data = {"chat_id": str(chat_id)}
    response = requests.get(url, headers=headers, json=data)
    
    if response.status_code == 200:
        response_dict = response.json()
        print("Успешный ответ:", response_dict)
        return response_dict
    else:
        print("Ошибка:", response.status_code, response.text)
