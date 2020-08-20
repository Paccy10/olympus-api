""" Module for testing publish and unpublish property endpoints """

from flask import json

import api.views.property
from api.utils.helpers.messages.success import (PROPERTY_PUBLISHED_MSG)
from api.utils.helpers.messages.error import (PROPERTY_ALREADY_PUBLISHED_MSG)
from ...constants import API_BASE_URL


class TestPublishProperty:
    """ Class for testing publish property endpoint """

    def test_publish_property_succeeds(self,
                                       client,
                                       init_db,
                                       unpublished_property,
                                       user_auth_header):
        """ Testing publish property """

        unpublished_property.save()
        response = client.patch(
            f'{API_BASE_URL}/properties/{unpublished_property.id}/publish',
            headers=user_auth_header)

        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['message'] == PROPERTY_PUBLISHED_MSG

    def test_publish_already_published_property_fails(self,
                                                      client,
                                                      init_db,
                                                      new_property,
                                                      user_auth_header):
        """ Testing publish an already published property """

        new_property.save()
        response = client.patch(
            f'{API_BASE_URL}/properties/{new_property.id}/publish',
            headers=user_auth_header)

        assert response.status_code == 400
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == PROPERTY_ALREADY_PUBLISHED_MSG
