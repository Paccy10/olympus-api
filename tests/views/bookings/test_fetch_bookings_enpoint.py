""" Module for testing fetch bookings endpoint """

from flask import json

import api.views.booking
from api.utils.helpers.messages.success import BOOKINGS_FETCHED_MSG
from ...constants import API_BASE_URL


class TestFetchBooking:
    """ Class for testing fetch bookings endpoint """

    def test_fetch_bookings_succeeds(self, client, init_db, admin_auth_header):
        """ Testing create booking """

        response = client.get(f'{API_BASE_URL}/bookings',
                              headers=admin_auth_header)

        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['message'] == BOOKINGS_FETCHED_MSG
        assert 'bookings' in response.json['data']
        assert 'metadata' in response.json['data']
