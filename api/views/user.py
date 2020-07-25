""" Module for users endpoints """

from flask import request
from flask_restx import Resource

from ..utils.helpers import request_data_strip
from ..utils.helpers import get_error_body
from ..utils.helpers.swagger.collections import user_namespace
from ..utils.helpers.swagger.models.user import signup_model, login_model
from ..utils.helpers.response import Response
from ..utils.helpers.messages.success import (USER_CREATED,
                                              USER_VERIFIED,
                                              USER_LOGGED_IN)
from ..utils.helpers.messages.error import (INVALID_USER_TOKEN_MSG,
                                            ALREADY_VERIFIED_MSG,
                                            INVALID_CREDENTIALS,
                                            USER_NOT_FOUND)
from ..utils.helpers.passwords_handler import hash_password, check_password
from ..utils.validators.user import UserValidators
from ..utils.send_email import send_email
from ..utils.tokens_handler import verify_user_token, generate_auth_token
from ..models.user import User
from ..schemas.user import UserSchema


@user_namespace.route('/signup')
class UserSignupResource(Resource):
    """" Resource class for user signup endpoint """

    @user_namespace.expect(signup_model)
    def post(self):
        """ Endpoint to create the user """

        request_data = request_data_strip(request.get_json())
        UserValidators.validate_signup(request_data)
        request_data['password'] = hash_password(request_data['password'])
        new_user = User(**request_data)
        new_user.save()
        user_schema = UserSchema(exclude=['password'])
        user_data = user_schema.dump(new_user)
        email_sent = send_email(
            user_data, 'Verification Email', 'verification_email.html')
        response_data = {
            'user': user_data,
            'email_sent': email_sent
        }
        return Response.success(USER_CREATED, response_data, 201)


@user_namespace.route('/<string:token>/verify')
class UserVerifyResource(Resource):
    """" Resource class for user verification endpoint """

    def get(self, token):
        """ Endpoint to verify the user """

        user = verify_user_token(token)
        if not user:
            return Response.error(
                [get_error_body(token, INVALID_USER_TOKEN_MSG, 'path', 'url')], 400)

        if user.is_verified:
            return Response.error(
                [get_error_body(user.is_verified,
                                ALREADY_VERIFIED_MSG, 'is_verified', '')], 400)

        user.update({'is_verified': True})
        user_schema = UserSchema(exclude=['password'])
        user_data = user_schema.dump(user)
        response_data = {
            'user': user_data
        }
        return Response.success(USER_VERIFIED, response_data, 200)


@user_namespace.route('/login')
class UserLoginResource(Resource):
    """" Resource class for user login endpoint """

    @user_namespace.expect(login_model)
    def post(self):
        """ Endpoint to login the user """

        request_data = request_data_strip(request.get_json())
        UserValidators.validate_login(request_data)
        user = User.find_user(request_data['username'])

        if not user:
            return Response.error(
                [get_error_body(request_data, USER_NOT_FOUND, '', '')], 404)

        user_schema = UserSchema()
        user_password = user_schema.dump(user)['password']

        if not check_password(request_data['password'], user_password):
            return Response.error(
                [get_error_body(request_data, INVALID_CREDENTIALS, '', 'body')], 404)

        user_schema = UserSchema(exclude=['password'])
        logged_in_user = user_schema.dump(user)
        token = generate_auth_token(logged_in_user['id'])
        response_data = {
            'token': token,
            'user': logged_in_user
        }
        return Response.success(USER_LOGGED_IN, response_data, 200)
