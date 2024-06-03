from uuid import uuid4

from firestore import client
from utils.security import *
from exceptions.user import *


def create_user(data) -> None:
    """
        Registra um novo usuário

    :param data: Os dados base, de usuário. Campos: 'password', 'email' e 'username'

    :raise EmailAlreadyRegisteredError: Se o email fornecido já estiver registrado
    """
    user_uuid = str(uuid4())
    collection = client.collection('users')

    exists = collection.where('email', '==', data.email).limit(1).get()

    if len(exists) > 0:
        raise EmailAlreadyRegisteredError()

    collection.document(user_uuid).set({
        'username': data.username,
        'email': data.email,
        'password': str(encode_password(data.password))
    })


def login_account(data) -> str:
    """
        Cria uma autenticação baseada em JWT, com tempo de 4 semanas de validade

    :param data:  São as credências. Campos: 'password' e 'email'

    :return: Um Token de autenticação JWT

    :raises:
        AuthNotPermissionError: Se a senha fornecida não estiver correta

        UserNotFoundError: Se o 'email' não for encontrado
    """
    collection = client.collection('users')

    query = collection.where('email', '==', data.email).limit(1)
    user_snapshot = query.get()

    if len(user_snapshot) == 0:
        raise UserNotFoundError()

    user_doc = user_snapshot[0]
    user_uuid = user_doc.id
    user_data = user_doc.to_dict()

    if not verify_password(data.password, user_data['password']):
        raise AuthNotPermissionError()

    if 'connections' not in user_data:
        user_data['connections'] = dict()

    connection = str(uuid4())

    token = JWTManager.encode(connection, user_uuid)

    connections = user_data['connections']
    connections[connection] = token['at']

    connections = clear_token_connections(connections)

    collection.document(user_uuid).update({'connections': connections})

    return token['token']


def refresh_token(token: Token) -> str:
    """
        Gera uma nova conexão com o usuário. Assim, invalidando o Token fornecido e gerando um novo.

    :param token: Token de autenticação atual

    :return: Retorna um Novo token gerado

    :raises:
        UserNotFoundError: Se não for encontrado o uuid de usuário fornecido pelo Token

        AuthNotPermissionError: Quando a conexão do Token (campo 'dest') não for encontrada na lista de conexões de
            usuário alvo
    """

    user_document = client.collection('users').document(token.uuid)
    user_document_data = user_document.get().to_dict()

    if not user_document.get().exists:
        raise UserNotFoundError()

    connections: Dict[str, str] = user_document_data['connections']
    connection = str(uuid4())

    if not is_authenticated_token(token, user_document_data['connections']):
        raise AuthNotPermissionError()

    new_token = JWTManager.encode(connection, token.uuid)

    del connections[token.dest]

    connections[connection] = new_token['at']
    connections = clear_token_connections(connections)

    user_document.update({'connections': connections})

    return new_token['token']
