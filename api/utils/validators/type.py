""" Module for type validators """

from flask import request

from . import (raise_bad_request_error,
               raise_conflict_error,
               validate_request_body,
               check_not_allowed_params)
from ..helpers import get_error_body
from ..helpers.messages.error import (TAKEN_TYPE_NAME_MSG,
                                      TYPE_NOT_FOUND_MSG)
from ...models.type import Type


class TypeValidators:
    """ Type validators class """

    @classmethod
    def validate_type_body(cls, data):
        """ Validates the type request body """

        validate_request_body(data, ['name'])
        check_not_allowed_params(data, ['name', 'description'])

    @classmethod
    def validate_create(cls, data: dict):
        """ Validates the type creation """

        cls.validate_type_body(data)
        name = data.get('name')
        property_type = Type.query.filter(
            Type.name == name.lower().strip()).first()

        if property_type:
            raise_conflict_error(
                [get_error_body(name, TAKEN_TYPE_NAME_MSG, 'name')])

    @classmethod
    def validate_update(cls, data: dict, type_id):
        """ Validates the type creation """

        cls.validate_type_body(data)
        name = data.get('name')
        property_type = Type.query.filter(
            Type.name == name.lower().strip()).first()

        if property_type and property_type.id != type_id:
            raise_conflict_error(
                [get_error_body(name, TAKEN_TYPE_NAME_MSG, 'name')])
