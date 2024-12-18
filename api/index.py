import json
import base64
import uuid
from kinopoisk_api import get_random_movie, get_random_movie_by_genre
from sessions import create_session, join_session, get_chat_ids
from process_opinion import update_opinion, check_match
from films import add_film_to_favorites, get_favorites, set_film_rating, get_my_ratings
from yandexgpt_api import get_yandexGPT_search_result

def handler(event, context):
    http_method = event.get('httpMethod')
    path = event.get('headers', {}).get('X-Request-Path', 'Unknown path')
    body_raw = event.get('body', '')

    try:
        if event.get('isBase64Encoded', False):
            body_decoded = base64.b64decode(body_raw).decode('utf-8')
            body = json.loads(body_decoded)
        else:
            body = json.loads(body_raw)
    except (json.JSONDecodeError, base64.binascii.Error):
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Invalid JSON or Base64 in request body'})
        }

    if path == 'create_session' and http_method == 'POST':
        chat_id = body.get('chat_id')
        user_name = body.get('user_name')

        if not chat_id or not user_name:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Missing required parameters: chat_id or user_name'})
            }

        try:
            session_id = create_session(
                chat_id=chat_id,
                owner_name=user_name
            )
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'session_id': session_id})
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': str(e)})
            }

    elif path == 'approve_session' and http_method == 'POST':
        chat_id = body.get('chat_id')
        user_name = body.get('user_name')
        session_id = body.get('session_id')

        if not chat_id or not user_name or not session_id:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Missing required parameters: chat_id, user_name, session_id'})
            }

        try:
            owner = join_session(
                chat_id=chat_id,
                name=user_name,
                session_id=session_id
            )
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(owner)
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': str(e)})
            }

    elif path == 'get_recommendation' and http_method == 'GET':
        random_movie = get_random_movie()
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': random_movie
        }

    elif path == 'send_recommendation_opinion' and http_method == 'POST':
        chat_id = body.get('chat_id')
        film_id = body.get('film_id')
        session_id = body.get('session_id')
        opinion = body.get('opinion')

        if not chat_id or not film_id or not session_id or not opinion:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Missing required parameters: chat_id, user_name, session_id, opinion'})
            }

        update_opinion(
            session_id,
            film_id,
            chat_id,
            opinion
        )

        result = check_match(session_id, film_id)
        chats_ids = get_chat_ids(session_id)
        print(chats_ids)
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': {'chat_id_1': chats_ids['chat_id_1'], 'chat_id_2': chats_ids['chat_id_2'], 'match': result}
        }

    elif path == 'check_match' and http_method == 'GET':
        # Проверка на совпадение
        session_id = event.get('queryStringParameters', {}).get('session_id')
        film_id = event.get('queryStringParameters', {}).get('film_id')
        match = True if session_id and film_id else False
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'match': match})
        }
    
    elif path == 'add_favorite' and http_method == 'POST':
        chat_id = body.get('chat_id')
        film_id = body.get('film_id')
        film_name = body.get('film_name')
        film_description = body.get('film_description')

        add_film_to_favorites(chat_id, film_id, film_name, film_description)

        return {'statusCode': 200}

    elif path == 'get_favorites' and http_method == 'GET': 
        chat_id = body.get('chat_id')

        result = get_favorites(chat_id)

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': {"result": result}
        }

    elif path == 'get_movies_by_description' and http_method == 'GET':
        description = body.get('description')

        result = get_yandexGPT_search_result(description)

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': {"result": result}
        }
    
    elif path == 'get_random_movie_by_genre' and http_method == 'GET': 
        genre = body.get('genre')
        random_movie = get_random_movie_by_genre(genre)
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': random_movie
        }

    elif path == 'send_rating' and http_method == 'POST':
        chat_id = body.get('chat_id')
        film_id = body.get('film_id')
        film_name = body.get('film_name')
        rating = body.get('rating')

        set_film_rating(chat_id, film_id, film_name, rating)

        return {'statusCode': 200}

    elif path == 'get_rating' and http_method == 'GET':
        chat_id = body.get('chat_id')

        result = get_my_ratings(chat_id)

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': {"result": result}
        }

    return {
        'statusCode': 405,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'error': 'Method Not Allowed'})
    }

