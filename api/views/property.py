""" Module for properties endpoints """

from datetime import datetime
from flask import request
from flask_restx import Resource

from ..middlewares.token_required import token_required
from ..middlewares.permission_required import (property_owner_permission_required,
                                               admin_permission_required)
from ..utils.helpers import request_data_strip
from ..utils.helpers import get_error_body
from ..utils.helpers.swagger.collections import property_namespace
from ..utils.helpers.swagger.responses import get_responses
from ..utils.helpers.swagger.models.property import (property_model)
from ..utils.helpers.swagger.models.booking import (booking_model)
from ..utils.helpers.response import Response
from ..utils.helpers.messages.success import (PROPERTY_CREATED_MSG,
                                              PROPERTIES_FETCHED_MSG,
                                              PROPERTY_FETCHED_MSG,
                                              PROPERTY_UPDATED_MSG,
                                              PROPERTY_DELETED_MSG,
                                              BOOKING_CREATED_MSG)
from ..utils.helpers.messages.error import (PROPERTY_NOT_FOUND_MSG)
from ..utils.helpers.constants import DATE_FORMAT
from ..utils.validators.property import PropertyValidators
from ..utils.validators.booking import BookingValidators
from ..utils.upload_image import upload_image, destroy_image
from ..utils.pagination_handler import paginate_resource
from ..models.property import Property
from ..models.booking import Booking
from ..schemas.property import PropertySchema
from ..schemas.booking import BookingSchema


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
        """ Endpoint to fetch published properties """

        property_schema = PropertySchema(many=True)
        condition = Property.is_published
        properties, metadata = paginate_resource(
            Property, property_schema, condition)
        response = {
            'properties': properties,
            'metadata': metadata
        }

        return Response.success(PROPERTIES_FETCHED_MSG, response, 200)


@property_namespace.route('/<int:property_id>')
class SinglePropertyResource(Resource):
    """" Resource class for single property endpoints """

    @property_namespace.doc(responses=get_responses(200, 404))
    def get(self, property_id):
        """ Endpoint to get single property """

        _property = Property.query.filter(
            Property.id == property_id, Property.is_published).first()

        if not _property:
            return Response.error(
                [get_error_body(property_id, PROPERTY_NOT_FOUND_MSG, 'property_id', 'url')], 404)

        property_schema = PropertySchema()
        response = {
            'property': property_schema.dump(_property)
        }

        return Response.success(PROPERTY_FETCHED_MSG, response, 200)

    @token_required
    @property_owner_permission_required
    @property_namespace.expect(property_model)
    @property_namespace.doc(responses=get_responses(200, 400, 401, 403, 404))
    def put(self, property_id):
        """ Endpoint to update property """

        request_data = request_data_strip(request.get_json())
        PropertyValidators.validate_update(request_data)

        _property = Property.query.filter(
            Property.id == property_id).first()
        _property.update(request_data)

        property_schema = PropertySchema()
        response = {
            'property': property_schema.dump(_property)
        }

        return Response.success(PROPERTY_UPDATED_MSG, response, 200)

    @token_required
    @property_owner_permission_required
    @property_namespace.doc(responses=get_responses(200, 401, 403, 404))
    def delete(self, property_id):
        """ Endpoint to delete property """

        _property = Property.query.filter(
            Property.id == property_id).first()

        for image in _property.images:
            destroy_image(image['public_id'])

        _property.delete()

        property_schema = PropertySchema()
        response = {
            'property': property_schema.dump(_property)
        }

        return Response.success(PROPERTY_DELETED_MSG, response, 200)


@property_namespace.route('/all')
class AllPropertiesResource(Resource):
    """" Resource class for all properties endpoint """

    @token_required
    @admin_permission_required
    @property_namespace.doc(responses=get_responses(200, 401, 403))
    def get(self):
        """ Endpoint to fetch all properties """

        property_schema = PropertySchema(many=True)
        properties, metadata = paginate_resource(
            Property, property_schema, True)
        response = {
            'properties': properties,
            'metadata': metadata
        }

        return Response.success(PROPERTIES_FETCHED_MSG, response, 200)


@property_namespace.route('/<int:property_id>/book')
class BookPropertyResource(Resource):
    """" Resource class for booking a property endpoint """

    @token_required
    @property_namespace.doc(responses=get_responses(200, 401, 404))
    def post(self, property_id):
        """ Endpoint to book a property """

        request_data = request_data_strip(request.get_json())
        BookingValidators.validate_property(property_id)
        BookingValidators.validate_create(request_data)

        _property = Property.query.filter(Property.id == property_id).first()
        user_id = request.decoded_token['user']['id']
        checkin_date = datetime.strptime(
            request_data['checkin_date'], DATE_FORMAT)
        checkout_date = datetime.strptime(
            request_data['checkout_date'], DATE_FORMAT)
        days_of_stay = abs((checkout_date - checkin_date).days)
        price = _property.price * days_of_stay

        request_data['user_id'] = user_id
        request_data['property_id'] = property_id
        request_data['checkin_date'] = checkin_date
        request_data['checkout_date'] = checkout_date
        request_data['price'] = price

        new_booking = Booking(**request_data)
        new_booking.save()
        booking_schema = BookingSchema()
        response_data = {
            'booking': booking_schema.dump(new_booking)
        }

        return Response.success(BOOKING_CREATED_MSG, response_data, 201)
