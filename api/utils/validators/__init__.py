"""" Module for common validators """

from flask import request
from werkzeug.exceptions import BadRequest, Conflict, Unauthorized

from ..helpers import get_error_body
from ..helpers.messages.error import (KEY_REQUIRED_MSG,
                                      KEY_NOT_ALLOWED_MSG,
                                      NOT_IMAGE_EXT_MSG,
                                      NOT_INTEGER_MSG,
                                      NOT_FLOAT_MSG)


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


def raise_auth_error(errors):
    """
    Raises authorization error

    Args:
        errors (list): list of errors
    Raises:
        (ValidationError): raise an exception
    """

    error = Unauthorized()
    error.data = {
        'status': 'error',
        'errors': errors
    }
    raise error


def validate_image(key, file):
    """
    Validates if the file is an image

    Args:
        key(str): key name
        file (file): file name
    Raises:
        (ValidationError): raises an exception
    """

    extensions = {'png', 'jpg', 'jpeg'}

    filename = file.filename

    if filename == '':
        raise_bad_request_error(
            [get_error_body(None, KEY_REQUIRED_MSG.format(key), key)])

    extension = filename.rsplit('.', 1)[1].lower()
    if '.' in filename and extension not in extensions:
        raise_bad_request_error(
            [get_error_body(None, NOT_IMAGE_EXT_MSG, key)])


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
                value, KEY_NOT_ALLOWED_MSG.format(prop), f'{prop}'))

    if len(errors) > 0:
        raise_bad_request_error(errors)


def validate_request_body(body, keys):
    """
    Validates request body keys and values

    Args:
        body (dict): request body
        keys (list): list of keys that should be provided
    Return:
        (list): list of errors
    """
    errors = []

    for key in keys:
        param = body.get(key)
        if not param or not param.strip():
            errors.append(get_error_body(
                param, KEY_REQUIRED_MSG.format(key), f'{key}'))

    if len(errors) > 0:
        raise_bad_request_error(errors)


def validate_positive_integer(key, value, location='body'):
    """
    Checks if the provided value is a positive integer

    Args:
        value (int): value to validate
    Raises:
        (ValidationError): raise an exception if the provided value is not a positive integer
    """

    try:
        if int(value) <= 0:
            raise_bad_request_error(
                [get_error_body(value, NOT_INTEGER_MSG.format(key), key, location)])
    except ValueError:
        raise_bad_request_error(
            [get_error_body(value, NOT_INTEGER_MSG.format(key), key, location)])


def validate_float(key, value):
    """
    Checks if the provided value is a float number

    Args:
        value (float): value to validate
    Raises:
        (ValidationError): raise an exception if the provided value is not a float number
    """

    try:
        float(value)
    except ValueError:
        raise_bad_request_error(
            [get_error_body(value, NOT_FLOAT_MSG.format(key), key)])
