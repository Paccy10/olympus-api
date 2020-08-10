""" Module for testing create property endpoint """

import os
from io import BytesIO
from flask import json

import api.views.property
from api.utils.helpers.messages.success import PROPERTY_CREATED_MSG
from api.utils.helpers.messages.error import (KEY_REQUIRED_MSG,
                                              KEY_NOT_ALLOWED_MSG,
                                              CATEGORY_NOT_FOUND_MSG,
                                              TYPE_NOT_FOUND_MSG,
                                              NOT_FLOAT_MSG,
                                              NOT_INTEGER_MSG)
from ...mocks.property import (VALID_PROPERTY,
                               INVALID_PROPERTY_WITH_UNEXISTED_CATEGORY,
                               INVALID_PROPERTY_WITH_UNEXISTED_TYPE,
                               INVALID_PROPERTY_WITH_STRING_LAT,
                               INVALID_PROPERTY_WITH_INVALID_BED_NUM,
                               INVALID_PROPERTY_WITHOUT_IMAGES)
from ...constants import API_BASE_URL, FORM_CONTENT_TYPE


class TestCreateProperty:
    """ Class for testing create property endpoint """

    file_dir = os.path.dirname(os.path.realpath('__file__'))
    filename = os.path.join(file_dir, 'tests/mocks/images/pytest.png')

    def test_create_property_succeeds(self,
                                      client,
                                      init_db,
                                      new_category,
                                      new_type,
                                      admin_auth_header):
        """ Testing create property """

        image = open(self.filename, 'rb')
        img_string_io = BytesIO(image.read())
        new_category.save()
        new_type.save()

        VALID_PROPERTY['images'] = (img_string_io, 'image.png')
        VALID_PROPERTY['category_id'] = new_category.id
        VALID_PROPERTY['type_id'] = new_type.id

        response = client.post(
            f'{API_BASE_URL}/properties',
            data=VALID_PROPERTY,
            content_type=FORM_CONTENT_TYPE,
            headers=admin_auth_header)
        image.close()

        assert response.status_code == 201
        assert response.json['status'] == 'success'
        assert response.json['message'] == PROPERTY_CREATED_MSG
        assert 'property' in response.json['data']
        assert response.json['data']['property']['title'] == VALID_PROPERTY['title']

    def test_create_property_with_unexisted_category_fails(self,
                                                           client,
                                                           init_db,
                                                           admin_auth_header):
        """ Testing create property with unexisted category """

        response = client.post(
            f'{API_BASE_URL}/properties',
            data=INVALID_PROPERTY_WITH_UNEXISTED_CATEGORY,
            content_type=FORM_CONTENT_TYPE,
            headers=admin_auth_header)

        assert response.status_code == 400
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == CATEGORY_NOT_FOUND_MSG

    def test_create_property_with_unexisted_type_fails(self,
                                                       client,
                                                       init_db,
                                                       new_category,
                                                       admin_auth_header):
        """ Testing create property with unexisted type """

        new_category.save()
        INVALID_PROPERTY_WITH_UNEXISTED_TYPE['category_id'] = new_category.id
        response = client.post(
            f'{API_BASE_URL}/properties',
            data=INVALID_PROPERTY_WITH_UNEXISTED_TYPE,
            content_type=FORM_CONTENT_TYPE,
            headers=admin_auth_header)

        assert response.status_code == 400
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == TYPE_NOT_FOUND_MSG

    def test_create_property_with_string_lat_fails(self,
                                                   client,
                                                   init_db,
                                                   new_category,
                                                   new_type,
                                                   admin_auth_header):
        """ Testing create property with string latitude """

        new_category.save()
        new_type.save()
        INVALID_PROPERTY_WITH_STRING_LAT['category_id'] = new_category.id
        INVALID_PROPERTY_WITH_STRING_LAT['type_id'] = new_type.id
        response = client.post(
            f'{API_BASE_URL}/properties',
            data=INVALID_PROPERTY_WITH_STRING_LAT,
            content_type=FORM_CONTENT_TYPE,
            headers=admin_auth_header)

        assert response.status_code == 400
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == NOT_FLOAT_MSG.format(
            'latitude')

    def test_create_property_invalid_bed_num_fails(self,
                                                   client,
                                                   init_db,
                                                   new_category,
                                                   new_type,
                                                   admin_auth_header):
        """ Testing create property with bed number """

        new_category.save()
        new_type.save()
        INVALID_PROPERTY_WITH_INVALID_BED_NUM['category_id'] = new_category.id
        INVALID_PROPERTY_WITH_INVALID_BED_NUM['type_id'] = new_type.id
        response = client.post(
            f'{API_BASE_URL}/properties',
            data=INVALID_PROPERTY_WITH_INVALID_BED_NUM,
            content_type=FORM_CONTENT_TYPE,
            headers=admin_auth_header)

        assert response.status_code == 400
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == NOT_INTEGER_MSG.format(
            'beds')

    def test_create_property_without_images_fails(self,
                                                  client,
                                                  init_db,
                                                  new_category,
                                                  new_type,
                                                  admin_auth_header):
        """ Testing create property without images """

        new_category.save()
        new_type.save()
        INVALID_PROPERTY_WITHOUT_IMAGES['category_id'] = new_category.id
        INVALID_PROPERTY_WITHOUT_IMAGES['type_id'] = new_type.id
        response = client.post(
            f'{API_BASE_URL}/properties',
            data=INVALID_PROPERTY_WITHOUT_IMAGES,
            content_type=FORM_CONTENT_TYPE,
            headers=admin_auth_header)

        assert response.status_code == 400
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == KEY_REQUIRED_MSG.format(
            'images')
