""" Module for hashing password helper """

import bcrypt

from .constants import ENCODING


def hash_password(password):
    """
    Hashes user password for security
    Args:
        password(str): user password

    Returns:
        hashed_password(str): hashed password
    """

    bytes_password = bytes(password, encoding=ENCODING)
    hashed_bytes_password = bcrypt.hashpw(bytes_password, bcrypt.gensalt(10))
    hashed_password = hashed_bytes_password.decode(ENCODING)

    return hashed_password


def check_password(password1, password2):
    """
    Checks if passwords match
    Args:
        password1(str): provided password
        password2(str): stored password

    Returns:
        (bool): True if they match and False else
    """

    bytes_password1 = bytes(password1, encoding=ENCODING)
    bytes_password2 = bytes(password2, encoding=ENCODING)

    if bcrypt.checkpw(bytes_password1, bytes_password2):
        return True
    return False
