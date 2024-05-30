from argon2 import PasswordHasher


_password_hash = PasswordHasher()


def encode_password(password: str) -> str:
    return _password_hash.hash(password)


def verify_password(password_literal: str, password_hash: str) -> bool:
    return _password_hash.verify(password_hash, password_literal)
