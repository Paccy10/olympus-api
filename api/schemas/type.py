""" Module for the Type Schema """

from marshmallow import fields

from .base import BaseSchema


class TypeSchema(BaseSchema):
    """ Type Schema Class """

    name = fields.String(required=True)
    description = fields.String(required=True)
