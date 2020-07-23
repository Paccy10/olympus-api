""" Module for the User Schema """

from marshmallow import fields

from .base import BaseSchema


class UserSchema(BaseSchema):
    """ User Schema Class """

    firstname = fields.String(required=True)
    lastname = fields.String(required=True)
    email = fields.String(required=True)
    username = fields.String(required=True)
    password = fields.String(required=False)
    is_admin = fields.Boolean(required=True)
    is_verified = fields.Boolean(required=True)
    about = fields.String(required=True)
    avatar = fields.Dict(required=True)
    phone_number = fields.String(required=True)
