import os
import ydb
import ydb.iam
import datetime
import string
import random

driver_config = ydb.DriverConfig(
    endpoint=os.getenv('YDB_ENDPOINT'), 
    database=os.getenv('YDB_DATABASE'),
    credentials=ydb.iam.MetadataUrlCredentials(),
)

driver = ydb.Driver(driver_config)
# Wait for the driver to become active for requests.
driver.wait(fail_fast=True, timeout=5)
# Create the session pool instance to manage YDB sessions.
pool = ydb.SessionPool(driver)

def randomword(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def select_all(tablename):
    # create the transaction and execute query.
    text = f"SELECT * FROM `{tablename}`;"
    return pool.retry_operation_sync(lambda s: s.transaction().execute(
        text,
        commit_tx=True,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
    ))

def insert_session(tablename, chat_id_owner, owner_name, status):
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
    query = f"""
    SELECT * FROM `{tablename}`
    WHERE session_id = '{session_id}';
    """

    result = pool.retry_operation_sync(lambda s: s.transaction().execute(
        query,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
    ))
    
    rows = result[0].rows
    print(rows)
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
    update_query = f"""
    UPDATE `{tablename}`
    SET 
        chat_id_user={chat_id_user}, 
        user_name='{user_name}', 
        status='{status}'
    WHERE session_id='{session_id}';"""
    
    pool.retry_operation_sync(lambda s: s.transaction().execute(
        update_query,
        commit_tx=True,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
    ))

def check_opinion_exists(tablename, session_id, film_id):
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
    # SQL-запрос для получения film_id и film_name по chat_id
    text = f"""
        SELECT 
            film_id, 
            film_name
        FROM `{tablename}`
        WHERE chat_id = {chat_id};
    """
    
    # Выполняем запрос в базу данных и возвращаем результат
    result = pool.retry_operation_sync(lambda s: s.transaction().execute(
        text,
        commit_tx=True,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
    ))

    # Обрабатываем результат
    films = []
    if result and result[0].rows:
        for row in result[0].rows:
            film_id = row["film_id"].decode('utf-8') if isinstance(row["film_id"], bytes) else row["film_id"]
            film_name = row["film_name"].decode('utf-8') if isinstance(row["film_name"], bytes) else row["film_name"]
            films.append({"film_id": film_id, "film_name": film_name})

    return films

def check_film_rating_exists(tablename, chat_id, film_id):
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
    # Сначала проверяем, существует ли запись
    if check_film_rating_exists(tablename, chat_id, film_id):
        # Если запись существует, обновляем рейтинг
        text = f"""
        UPDATE `{tablename}`
        SET rating = {rating}
        WHERE chat_id = {chat_id} AND film_id = '{film_id}';
        """
    else:
        # Если записи нет, выполняем вставку
        text = f"""
        INSERT INTO `{tablename}`
        SELECT
            {chat_id} as chat_id, 
            '{film_id}' as film_id,
            '{film_name}' as film_name,
            {rating} as rating;
        """
    
    # Выполняем запрос (обновление или вставку)
    pool.retry_operation_sync(lambda s: s.transaction().execute(
        text,
        commit_tx=True,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
    ))

    return {"success": "Rating updated or inserted successfully."}

def get_film_ratings_by_chat_id(tablename, chat_id):
    # Формируем SQL-запрос для получения всех оценок по chat_id
    text = f"""
    SELECT film_id, film_name, rating
    FROM `{tablename}`
    WHERE chat_id = {chat_id};
    """

    # Выполняем запрос и получаем результат
    result = pool.retry_operation_sync(lambda s: s.transaction().execute(
        text,
        commit_tx=True,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
    ))

    # Парсим результат
    ratings = []
    for row in result[0].rows:
        film_id = row["film_id"].decode('utf-8') if isinstance(row["film_id"], bytes) else row["film_id"]
        film_name = row["film_name"].decode('utf-8') if isinstance(row["film_name"], bytes) else row["film_name"]
        ratings.append({"film_id": film_id, "film_name": film_name, "rating": row["rating"]})

    return ratings
