""" Module for testing update and delete property endpoints """

from flask import json

import api.views.property
from api.utils.helpers.messages.success import (PROPERTY_UPDATED_MSG,
                                                PROPERTY_DELETED_MSG)
from api.utils.helpers.messages.error import (PROPERTY_NOT_FOUND_MSG,
                                              UNAUTHORIZED_MSG)
from ...mocks.property import (VALID_UPDATE_PROPERTY)
from ...constants import API_BASE_URL


class TestUpdateProperty:
    """ Class for testing update property endpoint """

    def test_update_property_succeeds(self,
                                      client,
                                      init_db,
                                      new_property,
                                      new_category,
                                      new_type,
                                      user_auth_header):
        """ Testing update property """

        new_property.save()
        new_category.save()
        new_type.save()
        VALID_UPDATE_PROPERTY['category_id'] = f'{new_category.id}'
        VALID_UPDATE_PROPERTY['type_id'] = f'{new_type.id}'
        property_data = json.dumps(VALID_UPDATE_PROPERTY)

        response = client.put(
            f'{API_BASE_URL}/properties/{new_property.id}',
            data=property_data, headers=user_auth_header)

        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['message'] == PROPERTY_UPDATED_MSG
        assert 'property' in response.json['data']
        assert response.json['data']['property']['title'] == VALID_UPDATE_PROPERTY['title']

    def test_update_property_with_unavailable_id_fails(self,
                                                       client,
                                                       init_db,
                                                       new_category,
                                                       new_type,
                                                       user_auth_header):
        """ Testing update property with unexisted ID """

        new_category.save()
        new_type.save()
        VALID_UPDATE_PROPERTY['category_id'] = f'{new_category.id}'
        VALID_UPDATE_PROPERTY['type_id'] = f'{new_type.id}'
        property_data = json.dumps(VALID_UPDATE_PROPERTY)

        response = client.put(
            f'{API_BASE_URL}/properties/100',
            data=property_data, headers=user_auth_header)

        assert response.status_code == 404
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == PROPERTY_NOT_FOUND_MSG

    def test_update_property_with_unauthorized_user_fails(self,
                                                          client,
                                                          init_db,
                                                          new_category,
                                                          new_type,
                                                          new_property,
                                                          another_user_auth_header):
        """ Testing update property with unauthorized user """

        new_property.save()
        new_category.save()
        new_type.save()
        VALID_UPDATE_PROPERTY['category_id'] = f'{new_category.id}'
        VALID_UPDATE_PROPERTY['type_id'] = f'{new_type.id}'
        property_data = json.dumps(VALID_UPDATE_PROPERTY)

        response = client.put(
            f'{API_BASE_URL}/properties/{new_property.id}',
            data=property_data, headers=another_user_auth_header)

        assert response.status_code == 403
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == UNAUTHORIZED_MSG


class TestDeleteProperty:
    """ Class for testing delete property endpoint """

    def test_delete_property_succeeds(self, client, init_db, new_property, user_auth_header):
        """ Testing delete property """

        new_property.save()
        response = client.delete(
            f'{API_BASE_URL}/properties/{new_property.id}', headers=user_auth_header)

        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['message'] == PROPERTY_DELETED_MSG
