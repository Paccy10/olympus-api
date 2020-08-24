""" Module for testing fetch bookings endpoint """

from flask import json

import api.views.booking
from api.utils.helpers.messages.success import (BOOKINGS_FETCHED_MSG,
                                                BOOKING_FETCHED_MSG)
from api.utils.helpers.messages.error import (BOOKING_NOT_FOUND_MSG,
                                              UNAUTHORIZED_MSG)
from ...constants import API_BASE_URL


class TestFetchBookings:
    """ Class for testing fetch bookings endpoints """

    def test_fetch_bookings_succeeds(self, client, init_db, admin_auth_header):
        """ Testing fetch bookings """

        response = client.get(f'{API_BASE_URL}/bookings',
                              headers=admin_auth_header)

        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['message'] == BOOKINGS_FETCHED_MSG
        assert 'bookings' in response.json['data']
        assert 'metadata' in response.json['data']

    def test_fetch_user_bookings_succeeds(self, client, init_db, admin_auth_header):
        """ Testing fetch bookings """

        response = client.get(f'{API_BASE_URL}/users/profile/bookings',
                              headers=admin_auth_header)

        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['message'] == BOOKINGS_FETCHED_MSG
        assert 'bookings' in response.json['data']

    def test_fetch_single_booking_succeeds(self, client, init_db, new_booking, admin_auth_header):
        """ Testing fetch single booking """

        new_booking.save()
        response = client.get(f'{API_BASE_URL}/bookings/{new_booking.id}',
                              headers=admin_auth_header)

        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['message'] == BOOKING_FETCHED_MSG
        assert 'booking' in response.json['data']
