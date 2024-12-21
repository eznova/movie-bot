import os
import ydb
import ydb.iam
import datetime
import string
import random

# Конфигурация драйвера для подключения к YDB
driver_config = ydb.DriverConfig(
    endpoint=os.getenv('YDB_ENDPOINT'), 
    database=os.getenv('YDB_DATABASE'),
    credentials=ydb.iam.MetadataUrlCredentials(),
)

# Создание экземпляра драйвера и ожидание его активации
driver = ydb.Driver(driver_config)
driver.wait(fail_fast=True, timeout=5)

# Создание пула сессий для управления сессиями YDB
pool = ydb.SessionPool(driver)

def randomword(length=10):
    """
    Генерирует случайное слово заданной длины.
    
    :param length: Длина генерируемого слова. По умолчанию 10.
    :return: Случайная строка из строчных латинских букв.
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def select_all(tablename):
    """
    Выполняет запрос для получения всех записей из таблицы YDB.
    
    :param tablename: Имя таблицы, из которой нужно выбрать все данные.
    :return: Результат запроса, включая все строки таблицы.
    """
    text = f"SELECT * FROM `{tablename}`;"
    return pool.retry_operation_sync(lambda s: s.transaction().execute(
        text,
        commit_tx=True,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
    ))

def insert_session(tablename, chat_id_owner, owner_name, status):
    """
    Вставляет новую сессию в таблицу YDB сгенерированным session_id.
    
    :param tablename: Имя таблицы для вставки данных.
    :param chat_id_owner: ID владельца чата.
    :param owner_name: Имя владельца.
    :param status: Статус сессии.
    :return: Сгенерированный session_id.
    """
    session_id = randomword()
    text = f"""INSERT INTO `{tablename}`
    SELECT
        '{session_id}' as session_id, 
        {chat_id_owner} as chat_id_owner,
        '{owner_name}' as owner_name,
        '{status}' as status;"""
    pool.retry_operation_sync(lambda s: s.transaction().execute(
        text,
        commit_tx=True,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
    ))

    return session_id

def insert_opinion(tablename, session_id, film_id, opinion, column):
    """
    Вставляет мнение о фильме для сессии в таблицу YDB.
    
    :param tablename: Имя таблицы для вставки.
    :param session_id: Идентификатор сессии.
    :param film_id: Идентификатор фильма.
    :param opinion: Мнение о фильме.
    :param column: Столбец для вставки мнения (owner_opinion или user_opinion).
    """
    text = f"""INSERT INTO `{tablename}`
    SELECT
        '{session_id}' as session_id, 
        '{film_id}' as film_id, 
        {opinion} as {column};"""
    pool.retry_operation_sync(lambda s: s.transaction().execute(
        text,
        commit_tx=True,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
    ))

def get_session_by_id(tablename, session_id):
    """
    Получает данные сессии по session_id из таблицы YDB.
    
    :param tablename: Имя таблицы для выполнения запроса.
    :param session_id: Идентификатор сессии.
    :return: Информация о сессии или None, если сессия не найдена.
    """
    query = f"""
    SELECT * FROM `{tablename}`
    WHERE session_id = '{session_id}';
    """

    result = pool.retry_operation_sync(lambda s: s.transaction().execute(
        query,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
    ))

    rows = result[0].rows
    if rows:
        row = rows[0]
        return {
            "session_id": row["session_id"],
            "chat_id_owner": row["chat_id_owner"],
            "chat_id_user": row.get("chat_id_user"),
            "owner_name": row["owner_name"],
            "user_name": row.get("user_name"),
            "status": row["status"]
        }
    else:
        return None

def update_session(tablename, session_id, chat_id_user, user_name, status='in_progress'):
    """
    Обновляет данные сессии по session_id в таблице YDB.
    
    :param tablename: Имя таблицы для обновления данных.
    :param session_id: Идентификатор сессии.
    :param chat_id_user: ID пользователя чата.
    :param user_name: Имя пользователя.
    :param status: Статус сессии (по умолчанию 'in_progress').
    """
    update_query = f"""
    UPDATE `{tablename}`
    SET 
        chat_id_user={chat_id_user}, 
        user_name='{user_name}', 
        status='{status}'
    WHERE session_id='{session_id}';
    """
    
    pool.retry_operation_sync(lambda s: s.transaction().execute(
        update_query,
        commit_tx=True,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
    ))

def check_opinion_exists(tablename, session_id, film_id):
    """
    Проверяет, существует ли мнение для указанной сессии и фильма.
    
    :param tablename: Имя таблицы.
    :param session_id: Идентификатор сессии.
    :param film_id: Идентификатор фильма.
    :return: True, если мнение существует, иначе False.
    """
    text = f"""
    SELECT owner_opinion, user_opinion
    FROM `{tablename}`
    WHERE session_id = '{session_id}' AND film_id = '{film_id}';
    """

    result = pool.retry_operation_sync(lambda s: s.transaction().execute(
        text,
        commit_tx=True,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
    ))

    rows = result[0].rows if result else []
    
    if not rows:
        return False

    for row in rows:
        if row["owner_opinion"] is not None or row["user_opinion"] is not None:
            return True

    return False

def update_opinion_db(tablename, session_id, film_id, column_name, new_opinion):
    """
    Обновляет мнение в базе данных.
    
    :param tablename: Имя таблицы для обновления мнения.
    :param session_id: Идентификатор сессии.
    :param film_id: Идентификатор фильма.
    :param column_name: Имя столбца (owner_opinion или user_opinion).
    :param new_opinion: Новое мнение для обновления.
    """
    text = f"""
    UPDATE `{tablename}`
    SET {column_name} = {new_opinion}
    WHERE session_id = '{session_id}' AND film_id = '{film_id}';
    """
    
    pool.retry_operation_sync(lambda s: s.transaction().execute(
        text,
        commit_tx=True,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
    ))

def check_both_opinions_true(tablename, session_id, film_id):
    """
    Проверяет, что оба мнения (владельца и пользователя) о фильме равны True.
    
    :param tablename: Имя таблицы.
    :param session_id: Идентификатор сессии.
    :param film_id: Идентификатор фильма.
    :return: True, если оба мнения равны True, False, если одно из мнений ложно или отсутствует, None, если мнений нет.
    """
    text = f"""
        SELECT 
            session_id, 
            film_id, 
            owner_opinion, 
            user_opinion
        FROM `{tablename}`
        WHERE session_id = '{session_id}' 
        AND film_id = '{film_id}';
    """
    
    result = pool.retry_operation_sync(lambda s: s.transaction().execute(
        text,
        commit_tx=True,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
    ))

    if result and result[0].rows:
        opinions = result[0].rows
        for opinion in opinions:
            owner_opinion = opinion['owner_opinion'] == b'true' if isinstance(opinion['owner_opinion'], bytes) else opinion['owner_opinion']
            user_opinion = opinion['user_opinion'] == b'true' if isinstance(opinion['user_opinion'], bytes) else opinion['user_opinion']
            
            if owner_opinion is None or user_opinion is None:
                return None
            
            if not owner_opinion or not user_opinion:
                return False
            
            if owner_opinion and user_opinion:
                return True
    
    return None

def insert_favorite(tablename, chat_id, film_id, film_name, film_description):
    """
    Добавляет фильм в избранное пользователя.
    
    :param tablename: Имя таблицы для вставки.
    :param chat_id: ID чата пользователя.
    :param film_id: Идентификатор фильма.
    :param film_name: Название фильма.
    :param film_description: Описание фильма.
    """
    text = f"""INSERT INTO `{tablename}`
    SELECT
        {chat_id} as chat_id, 
        '{film_id}' as film_id,
        '{film_name}' as film_name,
        '{film_description}' as film_description;"""

    pool.retry_operation_sync(lambda s: s.transaction().execute(
        text,
        commit_tx=True,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
    ))

def get_favorites_by_chat_id(tablename, chat_id):
    """
    Получает все избранные фильмы для пользователя по chat_id.
    
    :param tablename: Имя таблицы.
    :param chat_id: ID чата пользователя.
    :return: Список фильмов в избранном.
    """
    text = f"""
        SELECT 
            film_id, 
            film_name
        FROM `{tablename}`
        WHERE chat_id = {chat_id};
    """
    
    result = pool.retry_operation_sync(lambda s: s.transaction().execute(
        text,
        commit_tx=True,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
    ))

    films = []
    if result and result[0].rows:
        for row in result[0].rows:
            film_id = row["film_id"].decode('utf-8') if isinstance(row["film_id"], bytes) else row["film_id"]
            film_name = row["film_name"].decode('utf-8') if isinstance(row["film_name"], bytes) else row["film_name"]
            films.append({"film_id": film_id, "film_name": film_name})

    return films

def check_film_rating_exists(tablename, chat_id, film_id):
    """
    Проверяет, существует ли запись о рейтинге для фильма.
    
    :param tablename: Имя таблицы.
    :param chat_id: ID чата пользователя.
    :param film_id: Идентификатор фильма.
    :return: True, если рейтинг существует, иначе False.
    """
    text = f"""
    SELECT COUNT(*) as count
    FROM `{tablename}`
    WHERE chat_id = {chat_id} AND film_id = '{film_id}';
    """

    result = pool.retry_operation_sync(lambda s: s.transaction().execute(
        text,
        commit_tx=True,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
    ))

    count = result[0].rows[0]["count"]
    return count > 0


def insert_or_update_film_rating(tablename, chat_id, film_id, film_name, rating):
    """
    Вставляет или обновляет рейтинг фильма для пользователя.
    
    :param tablename: Имя таблицы.
    :param chat_id: ID чата пользователя.
    :param film_id: Идентификатор фильма.
    :param film_name: Название фильма.
    :param rating: Оценка фильма.
    :return: Статус операции.
    """
    if check_film_rating_exists(tablename, chat_id, film_id):
        # Обновление существующего рейтинга
        text = f"""
        UPDATE `{tablename}`
        SET rating = {rating}
        WHERE chat_id = {chat_id} AND film_id = '{film_id}';
        """
    else:
        # Вставка нового рейтинга
        text = f"""
        INSERT INTO `{tablename}`
        SELECT
            {chat_id} as chat_id, 
            '{film_id}' as film_id,
            '{film_name}' as film_name,
            {rating} as rating;
        """
    
    pool.retry_operation_sync(lambda s: s.transaction().execute(
        text,
        commit_tx=True,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
    ))

    return {"success": "Rating updated or inserted successfully."}

def get_film_ratings_by_chat_id(tablename, chat_id):
    """
    Получает все рейтинги фильмов для пользователя по chat_id.
    
    :param tablename: Имя таблицы.
    :param chat_id: ID чата пользователя.
    :return: Список фильмов с рейтингами.
    """
    text = f"""
    SELECT film_id, film_name, rating
    FROM `{tablename}`
    WHERE chat_id = {chat_id};
    """

    result = pool.retry_operation_sync(lambda s: s.transaction().execute(
        text,
        commit_tx=True,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
    ))

    ratings = []
    for row in result[0].rows:
        film_id = row["film_id"].decode('utf-8') if isinstance(row["film_id"], bytes) else row["film_id"]
        film_name = row["film_name"].decode('utf-8') if isinstance(row["film_name"], bytes) else row["film_name"]
        ratings.append({"film_id": film_id, "film_name": film_name, "rating": row["rating"]})

    return ratings
