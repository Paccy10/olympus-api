""" Module for the Property Schema """

from marshmallow import fields

from .base import BaseSchema


class PropertySchema(BaseSchema):
    """ Property Schema Class """

    owner_id = fields.Integer(required=True)
    category_id = fields.Integer(required=True)
    type_id = fields.Integer(required=True)
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
    availability = fields.Boolean(required=True)
    is_published = fields.Boolean(required=True)
