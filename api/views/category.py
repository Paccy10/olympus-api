""" Module for categories endpoints """

from flask import request
from flask_restx import Resource

from ..middlewares.token_required import token_required
from ..middlewares.permission_required import permission_required
from ..utils.helpers import request_data_strip
from ..utils.helpers import get_error_body
from ..utils.helpers.swagger.collections import category_namespace
from ..utils.helpers.swagger.responses import get_responses
from ..utils.helpers.swagger.models.category import (category_model)
from ..utils.helpers.response import Response
from ..utils.helpers.messages.success import (CATEGORY_CREATED_MSG)
from ..utils.validators.category import CategoryValidators
from ..models.category import Category
from ..schemas.category import CategorySchema


@category_namespace.route('')
class CategoryResource(Resource):
    """" Resource class for category endpoints """

    @token_required
    @permission_required
    @category_namespace.expect(category_model)
    @category_namespace.doc(responses=get_responses(201, 400, 401, 403, 409))
    def post(self):
        """ Endpoint to create the category """

        request_data = request_data_strip(request.get_json())
        CategoryValidators.validate_create(request_data)
        request_data['name'] = request_data['name'].lower()
        new_category = Category(**request_data)
        new_category.save()

        category_schema = CategorySchema()
        response = {
            'category': category_schema.dump(new_category)
        }

        return Response.success(CATEGORY_CREATED_MSG, response, 201)