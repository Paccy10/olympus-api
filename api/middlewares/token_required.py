""" Module for validating and decoding jwt """

from os import getenv
from functools import wraps
from flask import request
import jwt

from ..utils.helpers.response import Response
from ..utils.validators import get_error_body
from ..utils.validators import (raise_bad_request_error,
                                raise_auth_error)
from ..utils.helpers.messages.error import (NO_AUTH_TOKEN_MSG,
                                            INVALID_AUTH_TOKEN_MSG,
                                            NO_BEARER_IN_TOKEN_MSG,
                                            EXPIRED_AUTH_TOKEN_MSG)


def validate_token(token):
    """ Get the token from headers

        Args:
            None
        Returns:
            token (str): Bearer token
    """

    if not token:
        raise_auth_error(
            [get_error_body(token, NO_AUTH_TOKEN_MSG, 'Authorization', 'headers')])

    if not token.startswith('Bearer'):
        raise_bad_request_error(
            [get_error_body(token, NO_BEARER_IN_TOKEN_MSG, 'Authorization', 'headers')])

    if len(token.split(' ')) != 2:
        raise_bad_request_error(
            [get_error_body(token, INVALID_AUTH_TOKEN_MSG, 'Authorization', 'headers')])


def token_required(func):
    """ Authentication decorator. Validates and decodes token from the client

        Args:
            func (function): Function to be decorated
        Returns:
            decorated (function): Decorated function
    """

    @wraps(func)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization')
        validate_token(auth)

        try:
            token = auth.split(' ')[1]
            decoded_token = jwt.decode(token, getenv(
                'SECRET_KEY'), algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response.error(
                [get_error_body(token, EXPIRED_AUTH_TOKEN_MSG, 'Authorization', 'headers')], 401)

        except jwt.InvalidTokenError:
            return Response.error(
                [get_error_body(token, INVALID_AUTH_TOKEN_MSG, 'Authorization', 'headers')], 400)

        setattr(request, 'decoded_token', decoded_token)
        return func(*args, **kwargs)
    return decorated
