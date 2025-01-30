import hashlib

def hash_message(message: str) -> str:
    return hashlib.sha256(message.encode('utf-8')).hexdigest()
