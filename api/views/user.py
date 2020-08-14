""" Module for users endpoints """

from flask import request
from flask_restx import Resource

from ..middlewares.token_required import token_required
from ..middlewares.permission_required import admin_permission_required
from ..utils.helpers import request_data_strip
from ..utils.helpers import get_error_body
from ..utils.helpers.swagger.collections import user_namespace
from ..utils.helpers.swagger.responses import get_responses
from ..utils.helpers.swagger.models.user import (signup_model,
                                                 login_model,
                                                 password_reset_model,
                                                 password_reset_request_model,
                                                 profile_model)
from ..utils.helpers.response import Response
from ..utils.helpers.messages.success import (USER_CREATED_MSG,
                                              USER_VERIFIED_MSG,
                                              USER_LOGGED_IN_MSG,
                                              PASSWORD_RESET_LINK_SENT_MSG,
                                              PASSWORD_UPDATED_MSG,
                                              PROFILE_UPDATED_MSG,
                                              PROFILE_FETCHED_MSG,
                                              PROPERTIES_FETCHED_MSG)
from ..utils.helpers.messages.error import (INVALID_USER_TOKEN_MSG,
                                            ALREADY_VERIFIED_MSG,
                                            INVALID_CREDENTIALS,
                                            USER_NOT_FOUND_MSG)
from ..utils.helpers.passwords_handler import hash_password, check_password
from ..utils.validators.user import UserValidators
from ..utils.send_email import send_email
from ..utils.tokens_handler import verify_user_token, generate_auth_token
from ..utils.upload_image import upload_image, destroy_image
from ..utils.pagination_handler import paginate_resource
from ..models.user import User
from ..models.property import Property
from ..schemas.user import UserSchema
from ..schemas.property import PropertySchema


@user_namespace.route('/signup')
class UserSignupResource(Resource):
    """" Resource class for user signup endpoint """

    @user_namespace.expect(signup_model)
    @user_namespace.doc(responses=get_responses(201, 400, 409))
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

        return Response.success(USER_CREATED_MSG, response_data, 201)


@user_namespace.route('/<string:token>/verify')
class UserVerifyResource(Resource):
    """" Resource class for user verification endpoint """

    @user_namespace.doc(responses=get_responses(200, 400))
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

        return Response.success(USER_VERIFIED_MSG, response_data, 200)


@user_namespace.route('/login')
class UserLoginResource(Resource):
    """" Resource class for user login endpoint """

    @user_namespace.expect(login_model)
    @user_namespace.doc(responses=get_responses(200, 400, 404))
    def post(self):
        """ Endpoint to login the user """

        request_data = request_data_strip(request.get_json())
        UserValidators.validate_user_request_body(
            request_data, ['username', 'password'])
        user = User.find_user(request_data['username'])

        if not user:
            return Response.error(
                [get_error_body(None, USER_NOT_FOUND_MSG, '')], 404)

        if not check_password(request_data['password'], user.password):
            return Response.error(
                [get_error_body(None, INVALID_CREDENTIALS, '')], 404)

        user_schema = UserSchema(exclude=['password'])
        user_data = user_schema.dump(user)
        token = generate_auth_token(user_data['id'])
        response_data = {
            'token': token,
            'user': user_data
        }

        return Response.success(USER_LOGGED_IN_MSG, response_data, 200)


@user_namespace.route('/reset-password')
class UserResetPasswordResource(Resource):
    """" Resource class for user password reset """

    @user_namespace.expect(password_reset_request_model)
    @user_namespace.doc(responses=get_responses(200, 400, 404))
    def post(self):
        """ Endpoint to request password reset link """

        request_data = request_data_strip(request.get_json())
        UserValidators.validate_user_request_body(request_data, ['email'])
        user = User.find_user(request_data['email'])

        if not user:
            return Response.error(
                [get_error_body(None, USER_NOT_FOUND_MSG, '', '')], 404)

        user_schema = UserSchema(exclude=['password'])
        user_data = user_schema.dump(user)
        email_sent = send_email(
            user_data, 'Password Reset', 'password_reset_email.html')
        response_data = {
            'user': user_data,
            'email_sent': email_sent
        }

        return Response.success(PASSWORD_RESET_LINK_SENT_MSG, response_data, 200)

    @user_namespace.expect(password_reset_model)
    @user_namespace.doc(responses=get_responses(200, 400, 404))
    def patch(self):
        """ Endpoint to rest user password """

        request_data = request_data_strip(request.get_json())
        UserValidators.validate_password_reset(request_data)
        token = request_data['token']
        password = request_data['password']
        user = verify_user_token(token)

        if not user:
            return Response.error(
                [get_error_body(token, INVALID_USER_TOKEN_MSG, 'token')], 400)

        password = hash_password(password)

        user.update({'password': password})
        user_schema = UserSchema(exclude=['password'])
        user_data = user_schema.dump(user)
        response_data = {
            'user': user_data,
        }

        return Response.success(PASSWORD_UPDATED_MSG, response_data, 200)


@user_namespace.route('/profile')
class UserProfileResource(Resource):
    """" Resource class for user own profile """

    @token_required
    @user_namespace.doc(responses=get_responses(200, 401))
    def get(self):
        """ Endpoint to get own profile """
        user_id = request.decoded_token['user']['id']
        user = User.find_by_id(user_id)
        user_schema = UserSchema(exclude=['password'])
        response = {
            'user': user_schema.dump(user)
        }

        return Response.success(PROFILE_FETCHED_MSG, response, 200)

    @token_required
    @user_namespace.expect(profile_model)
    @user_namespace.doc(responses=get_responses(200, 400, 401))
    def put(self):
        """ Endpoint to update user profile """

        user_id = request.decoded_token['user']['id']
        user = User.find_by_id(user_id)

        request_data = request_data_strip(request.form.to_dict())
        UserValidators.validate_profile_update(request_data, user_id)

        if 'avatar' in request.files:
            if user.avatar:
                destroy_image(user.avatar['public_id'])
            avatar = upload_image(request.files['avatar'], 'olympus/users')
            request_data['avatar'] = avatar

        user.update(request_data)
        user_schema = UserSchema(exclude=['password'])
        response = {
            'user': user_schema.dump(user)
        }

        return Response.success(PROFILE_UPDATED_MSG, response, 200)


@user_namespace.route('/profile/<string:username>')
class SingleUserProfileResource(Resource):
    """" Resource class for user profile """

    @user_namespace.doc(responses=get_responses(200, 404))
    def get(self, username):
        """ Endpoint to get user profile by username """

        user = User.find_user(username)
        if not user:
            return Response.error(
                [get_error_body(username, USER_NOT_FOUND_MSG, 'username', 'url')], 404)

        user_schema = UserSchema(exclude=['password'])
        user_data = user_schema.dump(user)
        response_data = {
            'user': user_data
        }

        return Response.success(PROFILE_FETCHED_MSG, response_data, 200)


@user_namespace.route('/profile/properties')
class UserPropertiesResource(Resource):
    """" Resource class for user properties """

    @token_required
    @user_namespace.doc(responses=get_responses(200, 401))
    def get(self):
        """ Endpoint to get user properties """

        user_id = request.decoded_token['user']['id']
        property_schema = PropertySchema(many=True)
        condition = Property.owner_id == user_id
        properties, metadata = paginate_resource(
            Property, property_schema, condition)
        response = {
            'properties': properties,
            'metadata': metadata
        }

        return Response.success(PROPERTIES_FETCHED_MSG, response, 200)
