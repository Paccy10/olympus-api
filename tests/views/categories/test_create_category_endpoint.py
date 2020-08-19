""" Module for testing create category endpoint """

from flask import json

import api.views.category
from api.utils.helpers.messages.success import CATEGORY_CREATED_MSG
from api.utils.helpers.messages.error import (KEY_REQUIRED_MSG,
                                              KEY_NOT_ALLOWED_MSG,
                                              TAKEN_CATEGORY_NAME_MSG,
                                              UNAUTHORIZED_MSG,
                                              NOT_INTEGER_MSG,
                                              CATEGORY_NOT_FOUND_MSG)
from ...mocks.category import (VALID_CATEGORY,
                               INVALID_CATEGORY_WITHOUT_NAME,
                               INVALID_CATEGORY_WITH_NOT_ALLOWED_PARAM,
                               INVALID_CATEGORY_WITH_EXISTED_NAME,
                               INVALID_CATEGORY_WITH_INVALID_PARENT_ID,
                               INVALID_CATEGORY_WITH_UNEXISTED_PARENT_ID)
from ...constants import API_BASE_URL


class TestCreateCategory:
    """ Class for testing create category endpoint """

    def test_create_category_succeeds(self, client, init_db, admin_auth_header):
        """ Testing create category """

        category_data = json.dumps(VALID_CATEGORY)
        response = client.post(
            f'{API_BASE_URL}/categories', data=category_data, headers=admin_auth_header)

        assert response.status_code == 201
        assert response.json['status'] == 'success'
        assert response.json['message'] == CATEGORY_CREATED_MSG
        assert 'category' in response.json['data']
        assert response.json['data']['category']['name'] == VALID_CATEGORY['name']

    def test_create_category_with_non_admin_user_fails(self,
                                                       client,
                                                       init_db,
                                                       user_auth_header):
        """ Testing create category with a non admin user """

        category_data = json.dumps(VALID_CATEGORY)
        response = client.post(
            f'{API_BASE_URL}/categories', data=category_data, headers=user_auth_header)

        assert response.status_code == 403
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == UNAUTHORIZED_MSG

    def test_create_category_without_name_fails(self,
                                                client,
                                                init_db,
                                                admin_auth_header):
        """ Testing create category without category name """

        category_data = json.dumps(INVALID_CATEGORY_WITHOUT_NAME)
        response = client.post(
            f'{API_BASE_URL}/categories', data=category_data, headers=admin_auth_header)

        assert response.status_code == 400
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == KEY_REQUIRED_MSG.format(
            'name')

    def test_create_category_with_not_allowed_param_fails(self, client, init_db, admin_auth_header):
        """ Testing with a not allowed param """

        category_data = json.dumps(INVALID_CATEGORY_WITH_NOT_ALLOWED_PARAM)
        response = client.post(
            f'{API_BASE_URL}/categories', data=category_data, headers=admin_auth_header)

        assert response.status_code == 400
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['param'] == 'test'
        assert response.json['errors'][0]['message'] == KEY_NOT_ALLOWED_MSG.format(
            'test')

    def test_create_category_with_existed_name_fails(self, client, new_category, admin_auth_header):
        """ Testing with an existed category name """

        new_category.save()
        category_data = json.dumps(INVALID_CATEGORY_WITH_EXISTED_NAME)
        response = client.post(
            f'{API_BASE_URL}/categories', data=category_data, headers=admin_auth_header)

        assert response.status_code == 409
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == TAKEN_CATEGORY_NAME_MSG

    def test_create_category_with_invalid_parent_id_fails(self,
                                                          client,
                                                          init_db, admin_auth_header):
        """ Testing create category with invalid parent ID """

        category_data = json.dumps(INVALID_CATEGORY_WITH_INVALID_PARENT_ID)
        response = client.post(
            f'{API_BASE_URL}/categories', data=category_data, headers=admin_auth_header)
        print(response.json)
        assert response.status_code == 400
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == NOT_INTEGER_MSG.format(
            'parent_id')

    def test_create_category_with_unexisted_parent_id_fails(self,
                                                            client,
                                                            init_db, admin_auth_header):
        """ Testing create category with unexisted parent ID """

        category_data = json.dumps(INVALID_CATEGORY_WITH_UNEXISTED_PARENT_ID)
        response = client.post(
            f'{API_BASE_URL}/categories', data=category_data, headers=admin_auth_header)

        assert response.status_code == 404
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == CATEGORY_NOT_FOUND_MSG
