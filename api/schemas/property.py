""" Module for the Property Schema """

from marshmallow import fields

from .base import BaseSchema
from .user import UserSchema
from .category import CategorySchema
from .type import TypeSchema


class PropertySchema(BaseSchema):
    """ Property Schema Class """

    title = fields.String(required=True)
    summary = fields.String(required=True)
    address = fields.String(required=True)
    longitude = fields.Float(required=True)
    latitude = fields.Float(required=True)
    guests = fields.Integer(required=True)
    beds = fields.Integer(required=True)
    baths = fields.Integer(required=True)
    garages = fields.Integer(required=True)
    images = fields.List(fields.Dict(), required=True)
    video = fields.String(required=True)
    price = fields.Decimal(required=True, as_string=True)
    is_published = fields.Boolean(required=True)
    owner = fields.Nested(UserSchema(
        only=('firstname', 'lastname', 'username', 'phone_number', 'avatar')))
    category = fields.Nested(CategorySchema(only=('name', 'description')))
    property_type = fields.Nested(TypeSchema(only=('name', 'description')))
