""" Module for testing create booking endpoint """

from flask import json

import api.views.property
from api.utils.helpers.messages.success import BOOKING_CREATED_MSG
from api.utils.helpers.messages.error import (PROPERTY_NOT_FOUND_MSG,
                                              PROPERTY_NOT_AVAILABLE_MSG,
                                              INCORRECT_DATE_FORMAT_MSG,
                                              CHECKIN_DATE_MSG,
                                              CHECKOUT_DATE_MSG)
from ...mocks.booking import (VALID_BOOKING,
                              INVALID_BOOKING_WITH_INVALID_DATES,
                              INVALID_BOOKING_WITH_PAST_CHECKIN_DATE,
                              INVALID_BOOKING_WITH_LOWER_CHECKOUT_DATE)
from ...constants import API_BASE_URL


class TestCreateBooking:
    """ Class for testing create booking endpoint """

    def test_create_booking_succeeds(self, client, init_db, new_property, user_auth_header):
        """ Testing create booking """

        new_property.save()
        booking_data = json.dumps(VALID_BOOKING)
        response = client.post(
            f'{API_BASE_URL}/properties/{new_property.id}/book',
            data=booking_data, headers=user_auth_header)

        assert response.status_code == 201
        assert response.json['status'] == 'success'
        assert response.json['message'] == BOOKING_CREATED_MSG
        assert 'booking' in response.json['data']

    def test_create_booking_on_unexisted_property_fails(self, client, init_db, user_auth_header):
        """ Testing create booking on unexisted property """

        booking_data = json.dumps(VALID_BOOKING)
        response = client.post(
            f'{API_BASE_URL}/properties/100/book',
            data=booking_data, headers=user_auth_header)

        assert response.status_code == 404
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == PROPERTY_NOT_FOUND_MSG

    def test_create_booking_on_unavailable_property_fails(self,
                                                          client,
                                                          init_db,
                                                          new_booking,
                                                          user_auth_header):
        """ Testing create booking on unavailable property """

        new_booking.save()
        booking_data = json.dumps(VALID_BOOKING)
        response = client.post(
            f'{API_BASE_URL}/properties/1/book',
            data=booking_data, headers=user_auth_header)

        assert response.status_code == 400
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == PROPERTY_NOT_AVAILABLE_MSG

    def test_create_booking_with_invalid_dates_fails(self,
                                                     client,
                                                     init_db,
                                                     another_property,
                                                     user_auth_header):
        """ Testing create booking with invalid dates """

        another_property.save()
        booking_data = json.dumps(INVALID_BOOKING_WITH_INVALID_DATES)
        response = client.post(
            f'{API_BASE_URL}/properties/{another_property.id}/book',
            data=booking_data, headers=user_auth_header)
        print(response.json)
        assert response.status_code == 400
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == INCORRECT_DATE_FORMAT_MSG

    def test_create_booking_with_past_checkin_date_fails(self,
                                                         client,
                                                         init_db,
                                                         another_property,
                                                         user_auth_header):
        """ Testing create booking with past checkin date """

        another_property.save()
        booking_data = json.dumps(INVALID_BOOKING_WITH_PAST_CHECKIN_DATE)
        response = client.post(
            f'{API_BASE_URL}/properties/{another_property.id}/book',
            data=booking_data, headers=user_auth_header)

        assert response.status_code == 400
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == CHECKIN_DATE_MSG

    def test_create_booking_with_lower_checkout_date_fails(self,
                                                           client,
                                                           init_db,
                                                           another_property,
                                                           user_auth_header):
        """ Testing create booking with lower checkout date """

        another_property.save()
        booking_data = json.dumps(INVALID_BOOKING_WITH_LOWER_CHECKOUT_DATE)
        response = client.post(
            f'{API_BASE_URL}/properties/{another_property.id}/book',
            data=booking_data, headers=user_auth_header)

        assert response.status_code == 400
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == CHECKOUT_DATE_MSG
