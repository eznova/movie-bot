from process_database import select_all, insert_session, update_session, get_session_by_id

sessions_table = "movie_match/movie_sessions"

def check_sessions(chat_id):
    rows = select_all(sessions_table)

    sessions_found = []
    for row in rows:
        chat_id_owner = row["chat_id_owner"]
        chat_id_user = row["chat_id_user"]
        status = row["status"]

        if chat_id_to_check == chat_id_owner or chat_id_to_check == chat_id_user:
            sessions_found.append({"session_id": row["session_id"], "status": status})

    return sessions_found

def create_session(chat_id, owner_name):
    return insert_session(sessions_table, chat_id, owner_name,  "initiated")
    
def join_session(chat_id, name, session_id):
    update_session(sessions_table, session_id, chat_id, name)
    
    # Получаем строки результата
    rows = select_all(sessions_table)[0].rows
    
    for row in rows:
        # Проверяем и декодируем все байтовые данные
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
    session = get_session_by_id(sessions_table, session_id)
    value = {
        "chat_id_1": session['chat_id_owner'],
        "chat_id_2": session['chat_id_user'],
    }

    return value

    

