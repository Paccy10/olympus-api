""" Module for category validators """

from flask import request

from . import (raise_bad_request_error,
               raise_conflict_error,
               validate_request_body,
               validate_positive_integer,
               check_not_allowed_params)
from ..helpers import get_error_body
from ..helpers.messages.error import (TAKEN_CATEGORY_NAME_MSG,
                                      CATEGORY_NOT_FOUND_MSG)
from ...models.category import Category


class CategoryValidators:
    """ Category validators class """

    @classmethod
    def validate_subcategory(cls, parent_id):
        """
            Checks if the provided parent category exists

            Args:
                parent_id (int): category parent id
            Raises:
                (ValidationError): raises an exception if the parent id doesn't
                exist in the database
        """

        validate_positive_integer('parent_id', parent_id)

        category = Category.find_by_id(parent_id)

        if not category:
            raise_bad_request_error(
                [get_error_body(parent_id, CATEGORY_NOT_FOUND_MSG, 'parent_id')])

    @classmethod
    def validate_create(cls, data: dict):
        """ Validates the category creation """

        required_keys = ['name']
        optional_keys = ['description', 'parent_id']
        allowed_keys = required_keys + optional_keys

        validate_request_body(data, required_keys)
        check_not_allowed_params(data, allowed_keys)

        name = data.get('name')
        parent_id = data.get('parent_id')
        category = Category.query.filter(
            Category.name == name.lower().strip()).first()

        if category:
            raise_conflict_error(
                [get_error_body(name, TAKEN_CATEGORY_NAME_MSG, 'name')])

        if parent_id or parent_id == '':
            cls.validate_subcategory(parent_id)
