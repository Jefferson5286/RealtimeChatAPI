from typing import Dict
from datetime import datetime, timedelta

from config import env
from exceptions.jwt import InvalidJSONWebTokenError, ExpiredJSONWebToken

from argon2 import PasswordHasher
from jose import jwt
from jose.constants import ALGORITHMS
from jose.exceptions import JWTError
from pytz import utc
from fastapi import Request, HTTPException


_password_hash = PasswordHasher()


class Token:
    """ Representação abstraída de um token decodificado """
    def __init__(self, **kwargs: Dict[str, str]):
        self.uuid = kwargs.get('uuid')
        self.dest = kwargs.get('dest')
        self.at = kwargs.get('at')


def is_authenticated_token(token: Token, options: Dict[str, str]) -> bool:
    """
       Retorna se o token tem uma conexão com o usuário alvo

    :param token: Token de autenticação decodificado

    :param options: É a lista de conexões de um usuário

    :return: 'True' para existir conexão ou 'False' se não existir
    """
    return token.dest in options.keys()


class JWTManager:
    string_format = '%Y-%m-%d %H:%M:%S.%f'
    exp_time = timedelta(weeks=4)

    @classmethod
    def encode(cls, dest: str, uuid: str) -> Dict[str, str]:
        """
            Gera um novo token JWT

        :param dest: um protocolo de conexão existente em um usuário

        :param uuid: identificador de usuário

        :return: Um Token de autenticação codificado e a data de geração
        """
        claims = {
            'uuid': uuid,
            'dest': dest,
            'at': datetime.now(utc).strftime(cls.string_format)
        }

        token = jwt.encode(claims, env.SECRET_KEY)

        return {'token': token, 'at': claims['at']}

    @classmethod
    def decode(cls, token: str) -> Token:
        """
            Decodifica um Token de autenticação

        :param token: Token de autenticação codificado

        :return: retorna um objeto do tipo <Token>

        :raises:
            ExpiredJSONWebToken: Se o Token fornecido estiver expirado

            InvalidJSONWebTokenError: Caso não seja possível decodificar o Token fornecido. Será considerado inválido
        """
        try:
            data = jwt.decode(token, env.SECRET_KEY, [ALGORITHMS.HS256])

            at = datetime.strptime(data['at'], cls.string_format).replace(tzinfo=utc)
            now = datetime.now(utc)

            if (at + cls.exp_time) < now:
                raise ExpiredJSONWebToken()

            token = Token(uuid=data['uuid'], dest=data['dest'], at=data['at'])

            return token

        except JWTError:
            raise InvalidJSONWebTokenError()


def encode_password(password: str) -> str:
    """
        Gerar hash seguro de senha

    :param password: Senha

    :return: Retorna um hash da senha
    """
    return _password_hash.hash(password)


def verify_password(password_literal: str, password_hash: str) -> bool:
    """
        Verifica se a senha é válida

    :param password_literal: Senha para verificação

    :param password_hash: Hash da senha salvo

    :return: Se a senha é válida
    """
    return _password_hash.verify(password_hash, password_literal)


def clear_token_connections(connections: Dict[str, str]) -> Dict[str, str]:
    """
        Limpa todas as conexões expiradas de um usuário

    :param connections: Conexões de um usuário

    :return: Retorna um dicionário apenas com conexões ativas
    """
    conn: Dict[str, str] = dict()

    for connection, at in connections.items():
        date = datetime.strptime(at, JWTManager.string_format).replace(tzinfo=utc)

        if not (date + JWTManager.exp_time) < datetime.now(utc):
            conn.update({connection: at})

    return conn


def extract_token_request(request: Request) -> Token:
    """
        Extrair dados de um token de autenticação,

    :param request: requisição de um EndPoit

    :return: retorna um token decodificado

    :raises:
        HTTPException 401: Token inválido
        HTTPException 419: Token expirado
    """
    try:
        _token = request.headers['Authorization']
        return JWTManager.decode(_token)

    except InvalidJSONWebTokenError:
        raise HTTPException(401, 'Unauthorized! Invalid token.')

    except ExpiredJSONWebToken:
        raise HTTPException(419, 'Connection will expire! authenticate again.')
