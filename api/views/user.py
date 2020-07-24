""" Module for users endpoints """

from flask import request
from flask_restx import Resource

from ..utils.helpers import request_data_strip
from ..utils.helpers.swagger.collections import user_namespace
from ..utils.helpers.swagger.models.user import signup_model
from ..utils.helpers.response import Response
from ..utils.helpers.messages.success import USER_CREATED
from ..utils.helpers.hash_password import hash_pasword
from ..utils.validators.user import UserValidators
from ..utils.send_email import send_email
from ..models.user import User
from ..schemas.user import UserSchema


@user_namespace.route('/signup')
class UserSignupResource(Resource):
    """" Resource class for user signup endpoint """

    @user_namespace.expect(signup_model)
    def post(self):
        """ Endpoint to create the user """

        request_data = request_data_strip(request.get_json())
        UserValidators.validate(request_data)
        request_data['password'] = hash_pasword(request_data['password'])
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
