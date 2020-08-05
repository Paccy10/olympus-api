""" Module for testing update and delete type endpoints """

from flask import json

import api.views.type
from api.utils.helpers.messages.success import (TYPE_UPDATED_MSG,
                                                TYPE_DELETED_MSG)
from api.utils.helpers.messages.error import (TYPE_NOT_FOUND_MSG,
                                              TAKEN_TYPE_NAME_MSG)
from ...mocks.type import (VALID_TYPE,
                           INVALID_UPDATE_TYPE,)
from ...constants import API_BASE_URL


class TestUpdateType:
    """ Class for testing update type endpoint """

    def test_update_type_succeeds(self, client, init_db, new_type, admin_auth_header):
        """ Testing update type """

        new_type.save()
        type_data = json.dumps(VALID_TYPE)
        response = client.put(
            f'{API_BASE_URL}/types/{new_type.name}',
            data=type_data, headers=admin_auth_header)

        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['message'] == TYPE_UPDATED_MSG
        assert 'type' in response.json['data']
        assert response.json['data']['type']['name'] == VALID_TYPE['name']

    def test_update_type_with_unexisted_name_fails(self, client, init_db, admin_auth_header):
        """ Testing update type with unexisted name """

        type_data = json.dumps(VALID_TYPE)
        response = client.put(
            f'{API_BASE_URL}/types/good', data=type_data, headers=admin_auth_header)

        assert response.status_code == 404
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == TYPE_NOT_FOUND_MSG

    def test_update_type_with_existed_name_fails(self,
                                                 client,
                                                 new_type,
                                                 another_type,
                                                 admin_auth_header):
        """ Testing update type with an existed type name """

        new_type.save()
        another_type.save()
        type_data = json.dumps(INVALID_UPDATE_TYPE)
        response = client.put(
            f'{API_BASE_URL}/types/{new_type.name}',
            data=type_data, headers=admin_auth_header)

        assert response.status_code == 409
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == TAKEN_TYPE_NAME_MSG
