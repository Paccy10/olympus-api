""" Module for Swagger category models """

from flask_restx import fields

from ..collections import property_namespace

booking_model = property_namespace.model('Booking', {
    'checkin_date': fields.String(required=True, description='Booking checkin date'),
    'checkout_date': fields.String(required=True, description='Booking checkout date'),
})
