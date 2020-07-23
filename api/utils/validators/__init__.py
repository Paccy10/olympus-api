"""" Module for common validators """

from werkzeug.exceptions import BadRequest, Conflict

from ..helpers import get_error_body
from ..helpers.messages.error import KEY_REQUIRED_MSG, KEY_NOT_ALLOWED_MSG


def check_not_allowed_params(body, keys):
    """
    Checks body params that are not allowed

    Args:
        body (dict): request body
        keys (list): list of keys that should be provided
    Return:
        (list): list of errors
    """
    errors = []

    for prop, value in body.items():
        if prop not in keys:
            errors.append(get_error_body(
                value, KEY_NOT_ALLOWED_MSG.format(prop), f'{prop}', 'body'))

    return errors


def validate_request_body(body, keys):
    """
    Validates request body keys and values

    Args:
        body (dict): request body
        keys (list): list of keys that should be provided
    Return:
        (list): list of errors
    """
    errors = check_not_allowed_params(body, keys)

    for key in keys:
        param = body.get(key)
        if not param or not param.strip():
            errors.append(get_error_body(
                param, KEY_REQUIRED_MSG.format(key), f'{key}', 'body'))

    return errors


def raise_bad_request_error(errors):
    """
    Raises bad request error

    Args:
        errors (list): list of errors
    Raises:
        (ValidationError): raise an exception
    """

    error = BadRequest()
    error.data = {
        'status': 'error',
        'errors': errors
    }
    raise error


def raise_conflict_error(errors):
    """
    Raises conflict error

    Args:
        errors (list): list of errors
    Raises:
        (ValidationError): raise an exception
    """

    error = Conflict()
    error.data = {
        'status': 'error',
        'errors': errors
    }
    raise error
