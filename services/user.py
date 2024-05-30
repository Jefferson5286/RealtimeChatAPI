from uuid import uuid4
from datetime import datetime

from config import env
from firestore import client
from utils.security import verify_password, encode_password
from exceptions.user import *

from jose import jwt
from jose.constants import ALGORITHMS
from jose.exceptions import JWTError
from pytz import timezone


def create_user(data) -> None:
    user_id = str(uuid4())
    collection = client.collection('users')

    exists = collection.where('email', '==', data.email).limit(1).get()

    print(exists)

    if len(exists) > 0:
        raise EmailAlreadyRegisteredError()

    collection.document(user_id).set({
        'username': data.username,
        'email': data.email,
        'password': str(encode_password(data.password))
    })


def login_account(data) -> str:
    collection = client.collection('users')

    query = collection.where('email', '==', data.email).limit(1)
    user_snapshot = query.get()

    if len(user_snapshot) == 0:
        raise UserNotFoundError()

    user_doc = user_snapshot[0]
    user_id = user_doc.id
    user_data = user_doc.to_dict()

    if not verify_password(data.password, user_data['password']):
        raise AuthNotPermissionError()

    tz = timezone('America/Sao_Paulo')

    payload = {
        'email': user_data['email'],
        'id': user_id,
        'on': datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S.%f')
    }

    token = jwt.encode(payload, env.SECRET_KEY)

    return token


def refresh_token(token: str) -> str:
    try:
        data = jwt.decode(token, env.SECRET_KEY, algorithms=[ALGORITHMS.HS256])

        tz = timezone('America/Sao_Paulo')

        payload = {
            'email': data['email'],
            'id': data['id'],
            'on': datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S.%f')
        }

        new_token = jwt.encode(payload, env.SECRET_KEY)

        return new_token

    except JWTError:
        raise InvalidJSONWebTokenError()
