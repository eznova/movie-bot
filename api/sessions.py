from process_database import select_all, insert_session, update_session, get_session_by_id

sessions_table = "movie_match/movie_sessions"

def check_sessions(chat_id):
    """
    Проверяет наличие сессий для заданного chat_id.

    :param chat_id: ID чата для проверки.
    :return: Список сессий, связанных с указанным chat_id.
    """
    rows = select_all(sessions_table)

    sessions_found = []
    for row in rows:
        chat_id_owner = row["chat_id_owner"]
        chat_id_user = row["chat_id_user"]
        status = row["status"]

        if chat_id == chat_id_owner or chat_id == chat_id_user:
            sessions_found.append({"session_id": row["session_id"], "status": status})

    return sessions_found


def create_session(chat_id, owner_name):
    """
    Создает новую сессию с заданным владельцем.

    :param chat_id: ID чата владельца.
    :param owner_name: Имя владельца сессии.
    :return: Идентификатор созданной сессии.
    """
    return insert_session(sessions_table, chat_id, owner_name, "initiated")


def join_session(chat_id, name, session_id):
    """
    Присоединяет пользователя к сессии.

    :param chat_id: ID чата пользователя.
    :param name: Имя пользователя.
    :param session_id: Идентификатор сессии.
    :return: Данные о друге (владельце сессии), если сессия найдена, иначе None.
    """
    update_session(sessions_table, session_id, chat_id, name)
    
    # Получаем данные из таблицы после обновления
    rows = select_all(sessions_table)
    
    for row in rows:
        # Декодируем байтовые данные, если необходимо
        updated_session_id = row["session_id"].decode('utf-8') if isinstance(row["session_id"], bytes) else row["session_id"]
        owner_name = row["owner_name"].decode('utf-8') if isinstance(row["owner_name"], bytes) else row["owner_name"]
        friend_id = row["chat_id_owner"]

        # Проверка соответствия session_id
        if session_id == updated_session_id:
            value = {
                "friend_id": friend_id,
                "friend_name": owner_name,
            }
            return value
    
    return None


def get_chat_ids(session_id):
    """
    Получает chat_id для владельца и пользователя по session_id.

    :param session_id: Идентификатор сессии.
    :return: Словарь с chat_id владельца и пользователя.
    """
    session = get_session_by_id(sessions_table, session_id)
    value = {
        "chat_id_1": session['chat_id_owner'],
        "chat_id_2": session['chat_id_user'],
    }

    return value

    

