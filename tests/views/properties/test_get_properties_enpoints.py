""" Module for testing get properties endpoints """

import api.views.property
from api.utils.helpers.messages.success import (PROPERTIES_FETCHED_MSG)
from api.utils.helpers.messages.error import PROPERTY_NOT_FOUND_MSG
from ...constants import API_BASE_URL


class TestGetPropertiesEndpoints:
    """ Class for testing get properties endpoints """

    def test_get_all_properties_succeeds(self, client, init_db):
        """ Testing get all properties """

        response = client.get(f'{API_BASE_URL}/properties')

        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['message'] == PROPERTIES_FETCHED_MSG
        assert 'properties' in response.json['data']
        assert len(response.json['data']['properties']) == 0
