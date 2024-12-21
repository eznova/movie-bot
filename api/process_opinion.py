from process_database import insert_opinion, get_session_by_id, check_opinion_exists, \
                            check_both_opinions_true, update_opinion_db

sessions_table = "movie_match/movie_sessions"
opinion_table = "movie_match/movies_opinion"

def write_opinion(session_id, film_id, user_id, opinion):
    """
    Записывает мнение пользователя о фильме для заданной сессии в таблицу YDB.

    :param session_id: Идентификатор сессии, в которой пользователь оставляет мнение.
    :param film_id: Идентификатор фильма, о котором оставляется мнение.
    :param user_id: ID пользователя, который оставляет мнение.
    :param opinion: Мнение пользователя о фильме (например, "true" или "false").
    :return: None, если сессия не найдена или пользователь не найден в сессии.
    """
    user_id = int(user_id)
    session_data = get_session_by_id(sessions_table, session_id)

    if not session_data:
        print(f"Сессия с ID {session_id} не найдена.")
        return None

    if session_data['chat_id_owner'] == user_id:
        column_name = 'owner_opinion'
    elif session_data['chat_id_user'] == user_id:
        column_name = 'user_opinion'
    else:
        print(f"Пользователь с ID {user_id} не найден в сессии.")
        return None
    
    insert_opinion(
        tablename=opinion_table,
        session_id=session_id,
        film_id=film_id,
        opinion=opinion,
        column=column_name
    )


def check_opinion(session_id, film_id):
    """
    Проверяет, существует ли мнение о фильме для заданной сессии.

    :param session_id: Идентификатор сессии, для которой нужно проверить мнение.
    :param film_id: Идентификатор фильма, для которого нужно проверить мнение.
    :return: True, если мнение о фильме существует, иначе False.
    """
    return check_opinion_exists(opinion_table, session_id, film_id)


def update_opinion(session_id, film_id, user_id, new_opinion):
    """
    Обновляет мнение пользователя о фильме для заданной сессии в таблице YDB.

    :param session_id: Идентификатор сессии, в которой пользователь обновляет мнение.
    :param film_id: Идентификатор фильма, о котором обновляется мнение.
    :param user_id: ID пользователя, который обновляет мнение.
    :param new_opinion: Новое мнение пользователя о фильме (например, "true" или "false").
    :return: None, если сессия не найдена или пользователь не найден в сессии.
    """
    if not check_opinion(session_id, film_id):
        write_opinion(session_id, film_id, user_id, new_opinion)
        return

    user_id = int(user_id)
    session_data = get_session_by_id(sessions_table, session_id)

    if not session_data:
        print(f"Сессия с ID {session_id} не найдена.")
        return

    # Определяем, чье мнение обновляем (владелец или пользователь)
    if session_data['chat_id_owner'] == user_id:
        column_name = 'owner_opinion'
    elif session_data['chat_id_user'] == user_id:
        column_name = 'user_opinion'
    else:
        print(f"Пользователь с ID {user_id} не найден в сессии.")
        return

    update_opinion_db(opinion_table, session_id, film_id, column_name, new_opinion)
    print(f"Мнение о фильме {film_id} обновлено для сессии {session_id}.")


def check_match(session_id, film_id):
    """
    Проверяет, что оба мнения (владельца и пользователя) о фильме равны True.

    :param session_id: Идентификатор сессии, для которой нужно проверить мнения.
    :param film_id: Идентификатор фильма, для которого нужно проверить мнения.
    :return: True, если оба мнения равны True, иначе False, или None, если мнений нет.
    """
    return check_both_opinions_true(opinion_table, session_id, film_id)
