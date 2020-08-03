""" Module for testing get categories endpoints """

import api.views.category
from api.utils.helpers.messages.success import CATEGORIES_FETCHED_MSG
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
