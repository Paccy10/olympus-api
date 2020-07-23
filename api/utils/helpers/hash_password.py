""" Module for hashing password helper """

import bcrypt


def hash_pasword(password):
    """
    Hashes user password for security
    Args:
        password(str): user password

    Returns:
        hashed_password(str): hashed password
    """

    bytes_password = bytes(password, encoding='utf-8')
    hashed_bytes_password = bcrypt.hashpw(bytes_password, bcrypt.gensalt(10))
    hashed_password = hashed_bytes_password.decode('utf-8')

    return hashed_password
