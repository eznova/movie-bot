import requests
import os
import json
from urllib.parse import quote

headers = {
    "accept": "application/json",
    "X-API-KEY": "K3SEGRJ-KYZM8H8-HKG0PX2-R9D5ZE2"
}

def get_random_movie():
    """
    Получает случайный фильм с помощью API Kinopoisk.
    
    Отправляет запрос к API для получения случайного фильма с обязательными полями (название, описание, постер).
    
    :return: Словарь с информацией о фильме (id, название, описание, URL постера) или сообщение об ошибке
    """
    url = "https://api.kinopoisk.dev/v1.4/movie/random?notNullFields=name&notNullFields=poster.url&notNullFields=description"
    response = requests.get(url, headers=headers, timeout=30)
    
    if response.status_code == 200:
        data = response.json()

        value = {
            "film_id": data.get('id'),
            "name": data.get('name'),
            "description": data.get('description'),
            "poster_url": data.get('poster', {}).get('previewUrl')
        }

        return value
    else:
        return {"error": f"Request failed with status code {response.status_code}"}

def get_random_movie_by_genre(genre):
    """
    Получает случайный фильм по жанру с помощью API Kinopoisk.
    
    Отправляет запрос к API для получения случайного фильма в заданном жанре с обязательными полями (название, описание, постер).
    
    :param genre: Жанр фильма, по которому нужно получить результат
    :return: Словарь с информацией о фильме (id, название, описание, URL постера) или сообщение об ошибке
    """
    encoded_genre = quote(genre)  # Кодируем жанр
    url = f"https://api.kinopoisk.dev/v1.4/movie/random?notNullFields=name&notNullFields=poster.url&notNullFields=description&genres.name={encoded_genre}"
    
    response = requests.get(url, headers=headers, timeout=30)
    
    if response.status_code == 200:
        data = response.json()
        print('11===============')
        print(data)
        
        value = {
            "film_id": data.get('id'),
            "name": data.get('name'),
            "description": data.get('description'),
            "poster_url": data.get('poster', {}).get('previewUrl')
        }
        
        return value
    else:
        return {"error": f"Request failed with status code {response.status_code}"}
