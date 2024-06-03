from typing import Dict

from firestore import client
from exceptions.user import UserNotFoundError

from google.cloud.firestore_v1 import DocumentSnapshot
from google.cloud.firestore import CollectionReference


def get_account_data(uuid: str) -> Dict[str, str]:
    """
       Pegar dados de uma conta baseado em um UUID

    :param uuid: UUID de alvo

    :return: Retorna um Dict contando as informações exigidas

    :raise UserNotFoundError: Não existe referência baseada no UUID fornecido
    """

    collection: CollectionReference = client.collection('users')

    query = ['username', 'email', 'profile_image_uri']
    user_document: DocumentSnapshot = collection.document(uuid).get(query)

    if not user_document.exists:
        raise UserNotFoundError()

    user_data: Dict[str, str] = user_document.to_dict()
    user_data['uuid'] = user_document.id

    return user_data
