import hashlib


def get_sha256(input_string):
    """
    This method generates
    hash with SHA-256 algo
    """
    sha = hashlib.sha256()
    sha.update(input_string.encode('utf-8'))
    return sha.digest().hex()


def calc_hash(doc: dict) -> str:

    return hashlib.sha256(str(doc).encode()).hexdigest()