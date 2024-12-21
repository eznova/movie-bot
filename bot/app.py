from flask import Flask, request, jsonify
import json
import os
from index import handler  # Предполагается, что ваш код находится в файле index.py

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    """
    Эндпоинт для обработки входящих запросов.
    """
    # Имитация структуры события Yandex Cloud
    event = {
        "body": request.data.decode('utf-8'),
    }
    context = {}  # Контекст можно оставить пустым для локального тестирования

    # Вызов основного обработчика
    response = handler(event, context)

    # Возврат ответа
    return jsonify(response), response.get('statusCode', 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, debug=True)
