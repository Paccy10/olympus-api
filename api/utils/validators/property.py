""" Module for property validators """

from flask import request

from . import (raise_bad_request_error,
               raise_conflict_error,
               validate_request_body,
               validate_positive_integer,
               validate_float,
               validate_image,
               check_not_allowed_params)
from ..helpers import get_error_body
from ..helpers.messages.error import (USER_NOT_FOUND_MSG,
                                      TYPE_NOT_FOUND_MSG,
                                      CATEGORY_NOT_FOUND_MSG,
                                      KEY_REQUIRED_MSG)
from ...models.type import Type
from ...models.category import Category


class PropertyValidators:
    """ Property validators class """

    @classmethod
    def validate_property_body(cls, data):
        """ Validates the property request body """

        required_keys = ['category_id', 'type_id', 'title', 'address', 'longitude',
                         'latitude', 'guests', 'beds', 'baths', 'price']
        optional_keys = ['summary', 'garages', 'video']
        allowed_keys = required_keys + optional_keys
        validate_request_body(data, required_keys)
        check_not_allowed_params(data, allowed_keys)

    @classmethod
    def validate_category(cls, category_id):
        """ Validates the category ID """

        validate_positive_integer('category_id', category_id)

        category = Category.find_by_id(category_id)

        if not category:
            raise_bad_request_error(
                [get_error_body(category_id, CATEGORY_NOT_FOUND_MSG, 'category_id')])

    @classmethod
    def validate_type(cls, type_id):
        """ Validates the type ID """

        validate_positive_integer('type_id', type_id)

        property_type = Type.find_by_id(type_id)

        if not property_type:
            raise_bad_request_error(
                [get_error_body(type_id, TYPE_NOT_FOUND_MSG, 'type_id')])

    @classmethod
    def validate_create(cls, data: dict):
        """ Validates the property creation """

        cls.validate_property_body(data)
        cls.validate_category(data.get('category_id'))
        cls.validate_type(data.get('type_id'))
        validate_float('longitude', data.get('longitude'))
        validate_float('latitude', data.get('latitude'))
        validate_positive_integer('guests', data.get('guests'))
        validate_positive_integer('beds', data.get('beds'))
        validate_positive_integer('baths', data.get('baths'))

        if data.get('garages'):
            validate_positive_integer('garages', data.get('garages'))

        if not 'images' in request.files:
            raise_bad_request_error(
                [get_error_body(None, KEY_REQUIRED_MSG.format('images'), 'images')])

        for image in request.files.getlist('images'):
            validate_image('images', image)
