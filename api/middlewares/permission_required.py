""" Module for validating user permissions """

from functools import wraps
from flask import request

from ..models.user import User
from ..models.property import Property
from ..utils.helpers.response import Response
from ..utils.validators import get_error_body
from ..utils.helpers.messages.error import (UNAUTHORIZED_MSG,
                                            PROPERTY_NOT_FOUND_MSG)


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


def property_owner_permission_required(func):
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
        property_id = request.path.split('/')[-1]
        _property = Property.query.filter(
            Property.id == property_id).first()

        if not _property:
            return Response.error(
                [get_error_body(property_id, PROPERTY_NOT_FOUND_MSG, 'property_id', 'url')], 404)

        if not user.is_admin and user.id != _property.owner_id:
            return Response.error([get_error_body(user.username, UNAUTHORIZED_MSG, '', '')], 403)

        return func(*args, **kwargs)
    return decorated
