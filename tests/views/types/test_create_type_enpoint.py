""" Module for testing create type endpoint """

from flask import json

import api.views.type
from api.utils.helpers.messages.success import TYPE_CREATED_MSG
from api.utils.helpers.messages.error import (KEY_REQUIRED_MSG,
                                              KEY_NOT_ALLOWED_MSG,
                                              TAKEN_TYPE_NAME_MSG)
from ...mocks.type import (VALID_TYPE,
                           INVALID_TYPE_WITH_EXISTED_NAME)
from ...constants import API_BASE_URL


class TestCreateType:
    """ Class for testing create type endpoint """

    def test_create_type_succeeds(self, client, init_db, admin_auth_header):
        """ Testing create type """

        type_data = json.dumps(VALID_TYPE)
        response = client.post(
            f'{API_BASE_URL}/types', data=type_data, headers=admin_auth_header)

        assert response.status_code == 201
        assert response.json['status'] == 'success'
        assert response.json['message'] == TYPE_CREATED_MSG
        assert 'type' in response.json['data']
        assert response.json['data']['type']['name'] == VALID_TYPE['name']

    def test_create_type_with_existed_name_fails(self, client, new_type, admin_auth_header):
        """ Testing with an existed type name """

        new_type.save()
        type_data = json.dumps(INVALID_TYPE_WITH_EXISTED_NAME)
        response = client.post(
            f'{API_BASE_URL}/types', data=type_data, headers=admin_auth_header)

        assert response.status_code == 409
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == TAKEN_TYPE_NAME_MSG
