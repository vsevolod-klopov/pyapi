import hashlib


def get_password_hash(password: str) -> str:
    hash_object = hashlib.md5(password.encode())
    return hash_object.hexdigest()