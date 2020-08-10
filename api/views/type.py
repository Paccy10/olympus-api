""" Module for types endpoints """

from flask import request
from flask_restx import Resource

from ..middlewares.token_required import token_required
from ..middlewares.permission_required import admin_permission_required
from ..utils.helpers import request_data_strip
from ..utils.helpers import get_error_body
from ..utils.helpers.swagger.collections import type_namespace
from ..utils.helpers.swagger.responses import get_responses
from ..utils.helpers.swagger.models.type import (type_model)
from ..utils.helpers.response import Response
from ..utils.helpers.messages.success import (TYPE_CREATED_MSG,
                                              TYPES_FETCHED_MSG,
                                              TYPE_FETCHED_MSG,
                                              TYPE_UPDATED_MSG,
                                              TYPE_DELETED_MSG)
from ..utils.helpers.messages.error import (TYPE_NOT_FOUND_MSG)
from ..utils.validators.type import TypeValidators
from ..models.type import Type
from ..schemas.type import TypeSchema


@type_namespace.route('')
class TypeResource(Resource):
    """" Resource class for property types endpoints """

    @token_required
    @admin_permission_required
    @type_namespace.expect(type_model)
    @type_namespace.doc(responses=get_responses(201, 400, 401, 403, 409))
    def post(self):
        """ Endpoint to create the property type """

        request_data = request_data_strip(request.get_json())
        TypeValidators.validate_create(request_data)
        request_data['name'] = request_data['name'].lower()
        new_type = Type(**request_data)
        new_type.save()

        type_schema = TypeSchema()
        response = {
            'type': type_schema.dump(new_type)
        }

        return Response.success(TYPE_CREATED_MSG, response, 201)

    @type_namespace.doc(responses=get_responses(200))
    def get(self):
        """ Endpoint to get all types """

        type_schema = TypeSchema(many=True)
        types = type_schema.dump(Type.find_all())
        response = {
            'types': types
        }

        return Response.success(TYPES_FETCHED_MSG, response, 200)


@type_namespace.route('/<string:name>')
class SingleTypeResource(Resource):
    """" Resource class for single propty type endpoints """

    @type_namespace.doc(responses=get_responses(200, 404))
    def get(self, name):
        """ Endpoint to get single type """

        property_type = Type.query.filter_by(name=name).first()

        if not property_type:
            return Response.error(
                [get_error_body(name, TYPE_NOT_FOUND_MSG, 'name', 'url')], 404)

        type_schema = TypeSchema()
        response = {
            'type': type_schema.dump(property_type)
        }

        return Response.success(TYPE_FETCHED_MSG, response, 200)

    @token_required
    @admin_permission_required
    @type_namespace.expect(type_model)
    @type_namespace.doc(responses=get_responses(200, 400, 401, 403, 404, 409))
    def put(self, name):
        """ Endpoint to update type """

        property_type = Type.query.filter_by(name=name).first()

        if not property_type:
            return Response.error(
                [get_error_body(name, TYPE_NOT_FOUND_MSG, 'name', 'url')], 404)

        request_data = request_data_strip(request.get_json())
        TypeValidators.validate_update(request_data, property_type.id)

        property_type.update(request_data)
        type_schema = TypeSchema()
        response = {
            'type': type_schema.dump(property_type)
        }

        return Response.success(TYPE_UPDATED_MSG, response, 200)

    @token_required
    @admin_permission_required
    @type_namespace.doc(responses=get_responses(200, 401, 403, 404))
    def delete(self, name):
        """ Endpoint to delete type """

        property_type = Type.query.filter_by(name=name).first()

        if not property_type:
            return Response.error(
                [get_error_body(name, TYPE_NOT_FOUND_MSG, 'name', 'url')], 404)

        property_type.delete()
        type_schema = TypeSchema()
        response = {
            'type': type_schema.dump(property_type)
        }

        return Response.success(TYPE_DELETED_MSG, response, 200)
