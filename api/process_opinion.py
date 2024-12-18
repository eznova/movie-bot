from process_database import insert_opinion, get_session_by_id, check_opinion_exists, \
                            check_both_opinions_true, update_opinion_db

sessions_table = "movie_match/movie_sessions"
opinion_table = "movie_match/movies_opinion"

def write_opinion(session_id, film_id, user_id, opinion):
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
    return check_opinion_exists(opinion_table, session_id, film_id)

def update_opinion(session_id, film_id, user_id, new_opinion):
    if not check_opinion(session_id, film_id):
        write_opinion(session_id, film_id, user_id, new_opinion)
        return

    user_id = int(user_id)
    session_data = get_session_by_id(sessions_table, session_id)

    if not session_data:
        print(f"Сессия с ID {session_id} не найдена.")
        return

    # Определяем, чье мнение мы обновляем (владелец или пользователь)
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
    return check_both_opinions_true(opinion_table, session_id, film_id)
