""" Module for tokens handler """

from os import getenv
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous.exc import BadSignature
from dotenv import load_dotenv

from ..models.user import User

load_dotenv()


def generate_user_token(user_id, expiration_time=1800):
    """
    Generates the token for the user
    Args:
        user_id(int): user id
        expiration_time(int): expiration time

    Returns:
        token(str): a string Token
    """

    serializer = Serializer(getenv('SECRET_KEY'), expiration_time)
    token = serializer.dumps({'user_id': user_id}).decode('utf-8')
    return token


def verify_user_token(token):
    """
    Verifies if the user token is valid
    Args:
        token(str): user token

    Returns:
        user(User): user
    """

    serializer = Serializer(getenv('SECRET_KEY'))
    try:
        user_id = serializer.loads(token)['user_id']
    except BadSignature:
        return None

    return User.find_by_id(user_id)
