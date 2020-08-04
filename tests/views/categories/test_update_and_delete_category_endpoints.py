""" Module for testing update and delete category endpoints """

from flask import json

import api.views.category
from api.utils.helpers.messages.success import CATEGORY_UPDATED_MSG
from api.utils.helpers.messages.error import (CATEGORY_NOT_FOUND_MSG,
                                              TAKEN_CATEGORY_NAME_MSG)
from ...mocks.category import (VALID_CATEGORY,
                               INVALID_UPDATE_CATEGORY,
                               INVALID_CATEGORY_WITH_UNEXISTED_PARENT_ID)
from ...constants import API_BASE_URL


class TestUpdateCategory:
    """ Class for testing update category endpoint """

    def test_update_category_succeeds(self, client, init_db, new_category, admin_auth_header):
        """ Testing update category """

        new_category.save()
        category_data = json.dumps(VALID_CATEGORY)
        response = client.put(
            f'{API_BASE_URL}/categories/{new_category.name}',
            data=category_data, headers=admin_auth_header)

        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['message'] == CATEGORY_UPDATED_MSG
        assert 'category' in response.json['data']
        assert response.json['data']['category']['name'] == VALID_CATEGORY['name']

    def test_update_category_with_unexisted_name_fails(self, client, init_db, admin_auth_header):
        """ Testing update category with unexisted name """

        category_data = json.dumps(VALID_CATEGORY)
        response = client.put(
            f'{API_BASE_URL}/categories/good', data=category_data, headers=admin_auth_header)

        assert response.status_code == 404
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == CATEGORY_NOT_FOUND_MSG

    def test_update_category_with_existed_name_fails(self,
                                                     client,
                                                     new_category,
                                                     another_category,
                                                     admin_auth_header):
        """ Testing update category with an existed category name """

        new_category.save()
        another_category.save()
        category_data = json.dumps(INVALID_UPDATE_CATEGORY)
        response = client.put(
            f'{API_BASE_URL}/categories/{new_category.name}',
            data=category_data, headers=admin_auth_header)

        assert response.status_code == 409
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == TAKEN_CATEGORY_NAME_MSG

    def test_update_category_with_unexisted_parent_id_fails(self,
                                                            client,
                                                            init_db,
                                                            new_category,
                                                            admin_auth_header):
        """ Testing update category with unexisted parent ID """

        new_category.save()
        category_data = json.dumps(INVALID_CATEGORY_WITH_UNEXISTED_PARENT_ID)
        response = client.put(
            f'{API_BASE_URL}/categories/{new_category.name}',
            data=category_data, headers=admin_auth_header)

        assert response.status_code == 400
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == CATEGORY_NOT_FOUND_MSG
