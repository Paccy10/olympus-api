""" Module for testing get user profile endpoints """

import api.views.user
from api.utils.helpers.messages.success import PROFILE_FETCHED_MSG
from api.utils.helpers.messages.error import (USER_NOT_FOUND)
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

    def test_get_user_profile_succeeds(self, client, init_db, new_user):
        """ Testing Get user profile """

        new_user.save()
        new_user.update({'is_verified': True})
        response = client.get(
            f'{API_BASE_URL}/users/profile/{new_user.username}')

        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['message'] == PROFILE_FETCHED_MSG
        assert 'user' in response.json['data']

    def test_get_user_profile_with_unexisted_user_fails(self, client, init_db):
        """ Testing Get user profile """

        response = client.get(
            f'{API_BASE_URL}/users/profile/df')

        assert response.status_code == 404
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == USER_NOT_FOUND
