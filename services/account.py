from typing import Dict

from utils.security import Token, JsonWebToken
from firestore import client


def get_account_data_from_token(token: str) -> Dict[str, str]:
    collection = client.collection('users')
    token_data: Token = JsonWebToken.decode(token)


