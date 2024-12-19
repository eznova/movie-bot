# Телеграм-бот для выбора фильмов

![Logo](docs/logo.png)

## Состав команды

- **Афоничев Илья**
- **Знова Елизавета**
- **Шелухина Екатерина**

## Общее описание системы

Этот проект представляет собой Telegram-бота, который помогает пользователям выбирать фильмы как индивидуально, так и в группах. Бот предлагает фильмы на основе предпочтений, настроений и фильтров пользователей. С его помощью можно сохранять любимые фильмы, получать уведомления о новинках, узнавать расписания кинотеатров и даже проводить опросы для выбора фильма в группах.

## Функционал бота

### 1. Создание сеансов для совместного выбора фильмов
- Два пользователя (или больше) могут создавать сеанс, где они голосуют за предложенные фильмы. Когда голоса совпадают, система уведомляет о "матче".

### 2. Рекомендации фильмов
- Бот предлагает фильмы на основе жанра, года выпуска, рейтинга и других фильтров, соответствующих предпочтениям пользователя.

### 3. Сохранение "Избранного"
- Пользователи могут сохранять понравившиеся фильмы в список "Избранное" для последующего просмотра.

### 4. Уведомления о новинках
- Бот отправляет сообщения о новых фильмах, которые соответствуют предпочтениям пользователя.

### 5. Групповые опросы
- Возможность создать опрос в групповом чате, чтобы участники могли проголосовать за фильм.

### 6. Расписание сеансов в кинотеатрах
- Бот помогает найти ближайшие сеансы фильмов, интегрируясь с базами данных кинотеатров.

### 7. Трейлеры и рецензии
- Возможность получить ссылку на трейлер или обзор фильма.

### 8. Подбор фильмов по настроению
- Пользователь сообщает свое настроение (например, "хочу что-то веселое"), и бот предлагает соответствующий фильм.

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
