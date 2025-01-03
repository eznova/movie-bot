# Структура базы данных

Этот документ описывает структуру базы данных, используемую для хранения информации о сессиях, мнениях пользователей о фильмах, избранных фильмах и рейтингах.

## Таблица `movie_sessions`

Таблица `movie_sessions` хранит информацию о сессиях между владельцем и пользователем.

### Структура таблицы:
```sql
CREATE TABLE movie_sessions (
    session_id STRING,                -- Идентификатор сессии 
    chat_id_owner INT32,              -- ID владельца чата
    owner_name STRING,                -- Имя владельца чата
    chat_id_user INT32,               -- ID пользователя чата (может быть NULL)
    user_name STRING,                 -- Имя пользователя чата (может быть NULL)
    status STRING                     -- Статус сессии (например, 'in_progress')
) PRIMARY KEY (session_id);
```

### Описание полей:
- **session_id**: Уникальный идентификатор сессии.
- **chat_id_owner**: Идентификатор владельца чата.
- **owner_name**: Имя владельца чата.
- **chat_id_user**: Идентификатор пользователя чата (может быть NULL, если пользователь еще не присоединился к сессии).
- **user_name**: Имя пользователя чата (может быть NULL).
- **status**: Статус сессии (например, 'in_progress', 'completed').

---

## Таблица `movie_opinion`

Таблица `movie_opinion` хранит мнения владельца и пользователя по каждому фильму в рамках сессии.

### Структура таблицы:
```sql
CREATE TABLE movie_opinion (
    session_id STRING,                -- Идентификатор сессии (связь с `movie_sessions`)
    film_id STRING,                   -- Идентификатор фильма
    owner_opinion BOOLEAN,            -- Мнение владельца (TRUE/FALSE)
    user_opinion BOOLEAN,             -- Мнение пользователя (TRUE/FALSE)
    PRIMARY KEY (session_id, film_id)
);
```

### Описание полей:
- **session_id**: Идентификатор сессии, связывается с таблицей `movie_sessions`.
- **film_id**: Идентификатор фильма.
- **owner_opinion**: Мнение владельца (значение может быть `TRUE` или `FALSE`).
- **user_opinion**: Мнение пользователя (значение может быть `TRUE` или `FALSE`).

---

## Таблица `favorites_films`

Таблица `favorites_films` хранит избранные фильмы пользователя.

### Структура таблицы:
```sql
CREATE TABLE favorites_films (
    chat_id INT32,                    -- ID чата
    film_id STRING,                   -- Идентификатор фильма
    film_name STRING,                 -- Название фильма
    film_description STRING,          -- Описание фильма
    PRIMARY KEY (chat_id, film_id)
);
```

### Описание полей:
- **chat_id**: Идентификатор чата (связь с пользователем).
- **film_id**: Идентификатор фильма.
- **film_name**: Название фильма.
- **film_description**: Описание фильма.

---

## Таблица `movie_ratings`

Таблица `movie_ratings` хранит рейтинги фильмов, выставленные пользователями.

### Структура таблицы:
```sql
CREATE TABLE movie_ratings (
    chat_id INT32,                    -- ID чата
    film_id STRING,                   -- Идентификатор фильма
    film_name STRING,                 -- Название фильма
    rating INT32,                     -- Рейтинг фильма
    PRIMARY KEY (chat_id, film_id)
);
```

### Описание полей:
- **chat_id**: Идентификатор чата (связь с пользователем).
- **film_id**: Идентификатор фильма.
- **film_name**: Название фильма.
- **rating**: Рейтинг фильма, выставленный пользователем (целое число).

---

## Связи между таблицами:

- **Таблица `movie_sessions`**: Основная таблица, которая хранит информацию о сессиях между владельцем и пользователем.
- **Таблица `movie_opinion`**: Связана с таблицей `movie_sessions` через поле `session_id`, и с каждым фильмом через поле `film_id`. Хранит мнения владельца и пользователя по фильмам.
- **Таблица `favorites_films`**: Связана с пользователем через поле `chat_id` и хранит информацию о фильмах, которые были добавлены в избранное пользователем.
- **Таблица `movie_ratings`**: Хранит рейтинги фильмов, выставленные пользователями. Связана с пользователем через `chat_id` и с фильмом через `film_id`.


![ERD](https://www.plantuml.com/plantuml/png/hPB1IiGm48RlVOgXLzcBtdfQ1P45wOBklOHjLWDDicIcAzBwxgR6eNPeq8Dxss_oJxwPT8ka0lMsAxGZG-zGMdynka6DQBp34XJ24i5GGFnTVVzlJ0iLF1-UTlL3AXnV5KNQ-3UdGwpjwiFDTIfzeSOfgpEP7cKaajL45ASUP_XHY17ysRZennFCvDS1JgQpah8xzwZWRhz_lB-jsNAjzbFgf2u-6DBOJEtJOWM3OR4CtaDMYgdS3lDMup6OCoMdt9w28kDUaj22_ADEwiWT9WVnJOtZPkD7yKuLbFCRbPc8t64C9U5SGWmfpy_NJyV7OUs2D3m7kDLV0bljsjvsdm00)

---

## Примечания:

- Все таблицы используют `PRIMARY KEY` на сочетание ключевых полей, таких как `session_id`, `chat_id`, и `film_id`.
- Статус сессий в таблице `movie_sessions` может быть полезен для отслеживания текущего состояния взаимодействия между пользователем и владельцем (например, в процессе обсуждения или завершенная сессия).
- В таблице `movie_opinion` могут быть NULL-значения, если одна из сторон (владелец или пользователь) еще не оставила мнение по фильму.

---

## Заключение

Эта структура базы данных позволяет эффективно работать с сессиями, множественными мнениями о фильмах, избранными фильмами и рейтингами, предоставляя гибкость для обработки различных аспектов взаимодействия между пользователями.
