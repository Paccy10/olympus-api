""" Module for validating user permissions """

from functools import wraps
from flask import request

from ..models.user import User
from ..models.property import Property
from ..models.booking import Booking
from ..utils.helpers.response import Response
from ..utils.validators import get_error_body
from ..utils.helpers.messages.error import (UNAUTHORIZED_MSG,
                                            PROPERTY_NOT_FOUND_MSG,
                                            BOOKING_NOT_FOUND_MSG)


def admin_permission_required(func):
    """ Permission decorator. Validates if user is allowed to perform action

        Args:
            func (function): Function to be decorated
        Returns:
            decorated (function): Decorated function
    """

    @wraps(func)
    def decorated(*args, **kwargs):
        decoded_token = request.decoded_token
        user = User.find_by_id(decoded_token['user']['id'])

        if not user.is_admin:
            return Response.error([get_error_body(user.is_admin, UNAUTHORIZED_MSG, '', '')], 403)

        return func(*args, **kwargs)
    return decorated


def owner_permission_required(model, message, key):
    """ Permission decorator. Validates if user is allowed to perform action

        Args:
            model(class): Function to be decorated
            message(str): Resource not found message
            key(str): Not found key
        Returns:
            decorator (function): actual decorator function
    """

    def decorator(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            decoded_token = request.decoded_token
            user = User.find_by_id(decoded_token['user']['id'])
            resource_id = request.path.split('/')[4]
            resource = model.query.filter(
                model.id == resource_id).first()

            if not resource:
                return Response.error(
                    [get_error_body(resource_id, message, key, 'url')], 404)

            if not user.is_admin and user.id != resource.user_id:
                return Response.error([get_error_body(user.username,
                                                      UNAUTHORIZED_MSG, '', '')], 403)

            return func(*args, **kwargs)
        return decorated
    return decorator
