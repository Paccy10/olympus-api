""" Module for bookings endpoints """

from flask import request
from flask_restx import Resource

from ..middlewares.token_required import token_required
from ..middlewares.permission_required import (admin_permission_required,
                                               owner_permission_required)
from ..utils.helpers import request_data_strip
from ..utils.helpers import get_error_body
from ..utils.helpers.swagger.collections import booking_namespace
from ..utils.helpers.swagger.responses import get_responses
from ..utils.helpers.swagger.models.booking import (booking_model)
from ..utils.helpers.response import Response
from ..utils.helpers.messages.success import (BOOKINGS_FETCHED_MSG,
                                              BOOKING_FETCHED_MSG)
from ..utils.helpers.messages.error import (BOOKING_NOT_FOUND_MSG)
from ..utils.pagination_handler import paginate_resource
from ..models.booking import Booking
from ..schemas.booking import BookingSchema


@booking_namespace.route('')
class BookingResource(Resource):
    """" Resource class for booking endpoints """

    @token_required
    @admin_permission_required
    @booking_namespace.doc(responses=get_responses(200, 401, 403))
    def get(self):
        """ Endpoint to fetch all bookings """

        booking_schema = BookingSchema(many=True)
        bookings, metadata = paginate_resource(Booking, booking_schema, True)
        response = {
            'bookings': bookings,
            'metadata': metadata
        }

        return Response.success(BOOKINGS_FETCHED_MSG, response, 200)


@booking_namespace.route('/<int:booking_id>')
class SingleBookingResource(Resource):
    """" Resource class for single booking endpoints """

    @token_required
    @owner_permission_required(Booking, BOOKING_NOT_FOUND_MSG, 'booking_id')
    @booking_namespace.doc(responses=get_responses(200, 401, 403, 404))
    def get(self, booking_id):
        """ Endpoint to fetch single booking """

        booking = Booking.query.filter(Booking.id == booking_id).first()
        booking_schema = BookingSchema()
        response = {
            'booking': booking_schema.dump(booking)
        }

        return Response.success(BOOKING_FETCHED_MSG, response, 200)
