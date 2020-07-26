""" Module for Swagger user models """

from flask_restx import fields

from ..collections import user_namespace

signup_model = user_namespace.model('Signup', {
    'firstname': fields.String(required=True, description='User firstname'),
    'lastname': fields.String(required=True, description='User lastname'),
    'email': fields.String(required=True, description='User email'),
    'username': fields.String(required=True, description='User username'),
    'password': fields.String(required=True, description='User password')
})

login_model = user_namespace.model('Login', {
    'username': fields.String(required=True, description='User username or email'),
    'password': fields.String(required=True, description='User password')
})

Password_reset_request_model = user_namespace.model('Password Reset Request', {
    'email': fields.String(required=True, description='User email')
})

password_reset_model = user_namespace.model('Password Reset', {
    'token': fields.String(required=True, description='User given token'),
    'password': fields.String(required=True, description='User new password')
})
