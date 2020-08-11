""" Module for properties endpoints """

from flask import request
from flask_restx import Resource

from ..middlewares.token_required import token_required
from ..utils.helpers import request_data_strip
from ..utils.helpers import get_error_body
from ..utils.helpers.swagger.collections import property_namespace
from ..utils.helpers.swagger.responses import get_responses
from ..utils.helpers.swagger.models.property import (property_model)
from ..utils.helpers.response import Response
from ..utils.helpers.messages.success import (PROPERTY_CREATED_MSG,
                                              PROPERTIES_FETCHED_MSG,
                                              PROPERTY_FETCHED_MSG,
                                              PROPERTY_UPDATED_MSG,
                                              PROPERTY_DELETED_MSG)
from ..utils.helpers.messages.error import (PROPERTY_NOT_FOUND_MSG)
from ..utils.validators.property import PropertyValidators
from ..utils.upload_image import upload_image
from ..utils.pagination_handler import paginate_resource
from ..models.property import Property
from ..schemas.property import PropertySchema


@property_namespace.route('')
class PropertyResource(Resource):
    """" Resource class for property endpoints """

    @token_required
    @property_namespace.expect(property_model)
    @property_namespace.doc(responses=get_responses(201, 400, 401))
    def post(self):
        """ Endpoint to create the property """

        request_data = request_data_strip(request.form.to_dict())
        PropertyValidators.validate_create(request_data)
        images = []
        for image in request.files.getlist('images'):
            image_file = upload_image(image, '/olympus/properties')
            images.append(image_file)

        owner_id = request.decoded_token['user']['id']
        request_data['owner_id'] = owner_id
        request_data['images'] = images
        new_property = Property(**request_data)
        new_property.save()
        property_schema = PropertySchema()
        response_data = {
            'property': property_schema.dump(new_property)
        }

        return Response.success(PROPERTY_CREATED_MSG, response_data, 201)

    @property_namespace.doc(responses=get_responses(200))
    def get(self):
        """ Endpoint to get all properties """

        property_schema = PropertySchema(many=True)
        condition = Property.is_published
        properties, metadata = paginate_resource(
            Property, property_schema, condition)
        response = {
            'properties': properties,
            'metadata': metadata
        }

        return Response.success(PROPERTIES_FETCHED_MSG, response, 200)
