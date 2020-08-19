""" Module for the Booking Schema """

from marshmallow import fields

from .base import BaseSchema
from .user import UserSchema
from .property import PropertySchema


class BookingSchema(BaseSchema):
    """ Booking Schema Class """

    user = fields.Nested(UserSchema(
        only=('firstname', 'lastname', 'username', 'phone_number', 'avatar')))
    _property = fields.Nested(PropertySchema(exclude=(
        'id', 'created_at', 'updated_at', 'is_published', 'owner', 'category', 'property_type')))
    checkin_date = fields.DateTime(required=True)
    checkout_date = fields.DateTime(required=True)
    price = fields.Decimal(required=True, as_string=True)
    status = fields.String(required=True)
