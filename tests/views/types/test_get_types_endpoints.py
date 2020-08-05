""" Module for testing get types endpoints """

import api.views.type
from api.utils.helpers.messages.success import (TYPES_FETCHED_MSG,
                                                TYPE_FETCHED_MSG)
from api.utils.helpers.messages.error import TYPE_NOT_FOUND_MSG
from ...constants import API_BASE_URL


class TestGetTypesEndpoints:
    """ Class for testing get types endpoints """

    def test_get_all_types_succeeds(self, client, init_db):
        """ Testing get all types """

        response = client.get(f'{API_BASE_URL}/types')

        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['message'] == TYPES_FETCHED_MSG
        assert 'types' in response.json['data']
        assert len(response.json['data']['types']) == 0

    def test_get_single_type_succeeds(self, client, init_db, new_type):
        """ Testing get single type """

        new_type.save()
        response = client.get(f'{API_BASE_URL}/types/{new_type.name}')

        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['message'] == TYPE_FETCHED_MSG
        assert 'type' in response.json['data']

    def test_get_single_type_with_unexisted_name_fails(self, client, init_db):
        """ Testing get single type with unexisted name """

        response = client.get(f'{API_BASE_URL}/types/good')

        assert response.status_code == 404
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == TYPE_NOT_FOUND_MSG
