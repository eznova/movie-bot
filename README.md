# Телеграм-бот для выбора фильмов

![Logo](docs/logo.png)

## Состав команды

- **Афоничев Илья**
- **Знова Елизавета**
- **Шелухина Екатерина**

## Общее описание системы

MovieMatch — это интеллектуальный телеграм-бот, предназначенный для помощи пользователям в поиске, подборе и оценке фильмов. Система использует возможности Телеграма для предоставления персонализированных рекомендаций, а также предлагает дополнительные функции, которые облегчают выбор фильмов, улучшая опыт просмотра. Бот не только предлагает рекомендации, но и позволяет пользователям взаимодействовать с контентом, обмениваться рекомендациями и формировать коллекции любимых фильмов.

Документация на систему в разделе docs

- [Архитектура](docs/ARCH.md)
- [Описание БД](docs/DB.md)

## Установка и запуск

1. Создать две Cloud Function в Yandex Cloud:
- [Api](https://github.com/eznova/movie-bot/tree/main/api)
- [Bot](https://github.com/eznova/movie-bot/tree/main/bot)
   
2. Установить точку входа index.handler для каждой из функций

3. Настроить env
    ```python
    API_KEY=''
    FOLDER_ID=''
    YDB_DATABASE=''
    YDB_ENDPOINT=''
    KINOPOISK_API_KEY=''
    ```

4. Запустить функции
5. Проверить работу API в соответствии с описанием [Swagger](https://eznova.github.io/movie-bot/)

## Использование

1. После запуска бота, отправьте команду `/start` в чат с ботом для начала работы.
2. Используйте доступные команды и функции для создания сеансов, голосования и получения рекомендаций.