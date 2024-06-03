from typing import Dict

from utils.security import Token
from firestore import client
from exceptions.user import UserNotFoundError

from google.cloud.firestore_v1 import DocumentSnapshot
from google.cloud.firestore import CollectionReference


def get_account_data(token: Token) -> Dict[str, str]:
    collection: CollectionReference = client.collection('users')

    query = ['username', 'email', 'profile_image_uri']
    user_document: DocumentSnapshot = collection.document(token.uuid).get(query)

    if not user_document.exists:
        raise UserNotFoundError()

    user_data: Dict[str, str] = user_document.to_dict()
    user_data['uuid'] = user_document.id

    return user_data
