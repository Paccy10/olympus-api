""" Module for testing get user profile endpoints """

import api.views.user
from api.utils.helpers.messages.success import PROFILE_FETCHED_MSG
from api.utils.helpers.messages.error import (KEY_REQUIRED_MSG)
from ...constants import API_BASE_URL


class TestGetUserProfile:
    """ Class for testing get user profile resources """

    def test_get_own_profile_succeeds(self, client, init_db, user_auth_header):
        """ Testing Get own profile """

        response = client.get(f'{API_BASE_URL}/users/profile',
                              headers=user_auth_header)

        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['message'] == PROFILE_FETCHED_MSG
        assert 'user' in response.json['data']
