""" Module for Swagger property models """

from flask_restx import fields

from ..collections import property_namespace

property_model = property_namespace.model('Property', {
    'category_id': fields.Integer(required=True, description='Property Category ID'),
    'type_id': fields.Integer(required=True, description='Property Type ID'),
    'title': fields.String(required=True, description='Property title'),
    'summary': fields.String(required=False, description='Property summary'),
    'address': fields.String(required=True, description='Property address'),
    'longitude': fields.Float(required=True, description='Property longitude'),
    'latitude': fields.Float(required=True, description='Property latitude'),
    'beds': fields.Integer(required=True, description='Property beds'),
    'baths': fields.Integer(required=True, description='Property baths'),
    'garages': fields.Integer(required=True, description='Property garages'),
    'images': fields.String(required=True, description='Property images'),
    'video': fields.String(required=False, description='Property video'),
})
