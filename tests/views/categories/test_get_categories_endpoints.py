""" Module for testing get categories endpoints """

import api.views.category
from api.utils.helpers.messages.success import (CATEGORIES_FETCHED_MSG,
                                                CATEGORY_FETCHED_MSG)
from api.utils.helpers.messages.error import CATEGORY_NOT_FOUND_MSG
from ...constants import API_BASE_URL


class TestGetCategoriesEndpoints:
    """ Class for testing get categories endpoints """

    def test_get_all_categories_succeeds(self, client, init_db):
        """ Testing get all categories """

        response = client.get(f'{API_BASE_URL}/categories')

        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['message'] == CATEGORIES_FETCHED_MSG
        assert 'categories' in response.json['data']
        assert len(response.json['data']['categories']) == 0

    def test_get_single_category_succeeds(self, client, init_db, new_category):
        """ Testing get single category """

        new_category.save()
        response = client.get(f'{API_BASE_URL}/categories/{new_category.name}')

        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['message'] == CATEGORY_FETCHED_MSG
        assert 'category' in response.json['data']

    def test_get_single_category_with_unexisted_name_fails(self, client, init_db):
        """ Testing get single category with unexisted name """

        response = client.get(f'{API_BASE_URL}/categories/good')

        assert response.status_code == 404
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == CATEGORY_NOT_FOUND_MSG
