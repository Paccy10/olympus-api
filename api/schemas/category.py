""" Module for the Category Schema """

from marshmallow import fields

from .base import BaseSchema


class CategorySchema(BaseSchema):
    """ Category Schema Class """

    name = fields.String(required=True)
    description = fields.String(required=True)
    parent_id = fields.Integer(required=True)
    subcategories = fields.Nested(
        lambda: CategorySchema(only=('id', 'name', 'description'), many=True))
