""" Module for testing get properties endpoints """

import api.views.property
from api.utils.helpers.messages.success import (PROPERTIES_FETCHED_MSG,
                                                PROPERTY_FETCHED_MSG)
from api.utils.helpers.messages.error import PROPERTY_NOT_FOUND_MSG
from ...constants import API_BASE_URL


class TestGetPropertiesEndpoints:
    """ Class for testing get properties endpoints """

    def test_get_published_properties_succeeds(self, client, init_db):
        """ Testing get all published properties """

        response = client.get(f'{API_BASE_URL}/properties')

        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['message'] == PROPERTIES_FETCHED_MSG
        assert 'properties' in response.json['data']
        assert len(response.json['data']['properties']) == 0

    def test_get_single_property_succeeds(self, client, init_db, new_property):
        """ Testing get single property """

        new_property.save()
        response = client.get(f'{API_BASE_URL}/properties/{new_property.id}')

        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['message'] == PROPERTY_FETCHED_MSG
        assert 'property' in response.json['data']

    def test_get_single_property_with_unexisted_id_fails(self, client, init_db):
        """ Testing get single property with unexisted id """

        response = client.get(f'{API_BASE_URL}/properties/100')

        assert response.status_code == 404
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == PROPERTY_NOT_FOUND_MSG

    def test_get_all_properties_succeeds(self, client, init_db, admin_auth_header):
        """ Testing get all properties """

        response = client.get(f'{API_BASE_URL}/properties/all',
                              headers=admin_auth_header)

        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['message'] == PROPERTIES_FETCHED_MSG
        assert 'properties' in response.json['data']
