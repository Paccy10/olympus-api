""" Module for types endpoints """

from flask import request
from flask_restx import Resource

from ..middlewares.token_required import token_required
from ..middlewares.permission_required import permission_required
from ..utils.helpers import request_data_strip
from ..utils.helpers import get_error_body
from ..utils.helpers.swagger.collections import type_namespace
from ..utils.helpers.swagger.responses import get_responses
from ..utils.helpers.swagger.models.type import (type_model)
from ..utils.helpers.response import Response
from ..utils.helpers.messages.success import (TYPE_CREATED_MSG)
from ..utils.helpers.messages.error import (TYPE_NOT_FOUND_MSG)
from ..utils.validators.type import TypeValidators
from ..models.type import Type
from ..schemas.type import TypeSchema


@type_namespace.route('')
class TypeResource(Resource):
    """" Resource class for category endpoints """

    @token_required
    @permission_required
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
