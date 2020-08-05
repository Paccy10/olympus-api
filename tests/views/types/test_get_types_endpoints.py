""" Module for testing get types endpoints """

import api.views.type
from api.utils.helpers.messages.success import (TYPES_FETCHED_MSG)
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
