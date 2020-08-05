""" Module for Swagger category models """

from flask_restx import fields

from ..collections import type_namespace

type_model = type_namespace.model('Type', {
    'name': fields.String(required=True, description='Type name'),
    'description': fields.String(required=False, description='Type description')
})
