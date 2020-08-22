""" Module for booking validators """

from datetime import datetime
from flask import request

from . import (raise_bad_request_error,
               raise_not_found_error,
               validate_request_body,
               validate_date,
               check_not_allowed_params)
from ..helpers import get_error_body
from ..helpers.messages.error import (CHECKIN_DATE_MSG,
                                      CHECKOUT_DATE_MSG,
                                      PROPERTY_NOT_FOUND_MSG,
                                      PROPERTY_NOT_AVAILABLE_MSG)
from ..helpers.constants import DATE_FORMAT
from ..helpers.response import Response
from ...models.booking import Booking
from ...models.property import Property


class BookingValidators:
    """ Booking validators class """

    @classmethod
    def validate_property(cls, property_id, checkin_date):
        """ Validates the booking property """

        _property = Property.query.filter(
            Property.id == property_id, Property.is_published).first()

        if not _property:
            raise_not_found_error(
                [get_error_body(property_id, PROPERTY_NOT_FOUND_MSG, 'property_id', 'url')])

        booking = Booking.query.filter(
            Booking.property_id == property_id, Booking.status == 'open').first()

        if booking and booking.checkout_date >= checkin_date:
            raise_bad_request_error(
                [get_error_body(property_id, PROPERTY_NOT_AVAILABLE_MSG, 'property_id', 'url')])

    @classmethod
    def validate_create(cls, data: dict):
        """ Validates the booking creation """

        keys = ['checkin_date', 'checkout_date']

        validate_request_body(data, keys)
        check_not_allowed_params(data, keys)
        validate_date('checkin_date', data.get('checkin_date'))
        validate_date('checkout_date', data.get('checkout_date'))

        checkin_date = datetime.strptime(data.get('checkin_date'), DATE_FORMAT)
        checkout_date = datetime.strptime(
            data.get('checkout_date'), DATE_FORMAT)

        if checkin_date.date() < datetime.today().date():
            raise_bad_request_error(
                [get_error_body(data.get('checkin_date'), CHECKIN_DATE_MSG, 'checkin_date')])

        if checkin_date >= checkout_date:
            raise_bad_request_error(
                [get_error_body(data.get('checkout_date'), CHECKOUT_DATE_MSG, 'checkout_date')])
