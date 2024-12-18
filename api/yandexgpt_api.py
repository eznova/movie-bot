import os
import requests
import json

# Получаем значения FOLDER_ID и API_KEY из переменных окружения
folder_id = os.getenv('FOLDER_ID')
api_key = os.getenv('API_KEY')

def get_yandexGPT_search_result(film_description):
    prompt = {
        "modelUri": f"gpt://{folder_id}/yandexgpt-lite",  # Форматируем строку с использованием f-строк
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "system",
                "text": "Ты ассистент который помогает с подбором того что посмотреть, выдвавй 5 тайтлов с описанием чтобы я мог выбрать"
            },
            {
                "role": "user",
                "text": f"Привет! Мне нужна твоя помощь, хочу чтобы ты мне выдал фильмы по описанию {film_description}"  # Форматируем строку
            },
        ]
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {api_key}"  # Форматируем строку
    }

    # Отправляем POST-запрос
    response = requests.post(url, headers=headers, json=prompt)

    # Проверяем статус ответа
    if response.status_code != 200:
        print("Ошибка API:", response.status_code, response.text)
        return None

    # Парсим JSON-ответ
    data = response.json()

    # Проверяем наличие ключа "result" в ответе
    if "result" not in data:
        print("Ключ 'result' отсутствует в ответе:", data)
        return None

    # Извлекаем основной текст из ответа
    main_text = data["result"]["alternatives"][0]["message"]["text"]
    return main_text
