""" Module for testing fetch users endpoints """

import api.views.user
from api.utils.helpers.messages.success import (USERS_FETCHED_MSG)
from ...constants import API_BASE_URL


class TestFtechUsers:
    """ Class for testing fetch users resource """

    def test_fetch_users_succeeds(self, client, init_db, admin_auth_header):
        """ Testing fetch all users """

        response = client.get(f'{API_BASE_URL}/users',
                              headers=admin_auth_header)

        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['message'] == USERS_FETCHED_MSG
        assert 'users' in response.json['data']
