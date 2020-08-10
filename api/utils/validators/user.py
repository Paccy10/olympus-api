""" Module for user validators """

import re

from flask import request
from . import (raise_bad_request_error,
               raise_conflict_error,
               validate_request_body,
               check_not_allowed_params,
               validate_image)
from ..helpers import get_error_body
from ..helpers.messages.error import (INVALID_EMAIL_MSG,
                                      WEAK_PASSWORD_MSG,
                                      TAKEN_EMAIL_MSG,
                                      TAKEN_USERNAME_MSG,
                                      INVALID_PHONE_MSG,
                                      TAKEN_PHONE_MSG,
                                      KEY_REQUIRED_MSG)
from ...models.user import User


class UserValidators:
    """ User validators class """

    @classmethod
    def validate_email(cls, email):
        """
        Checks if the provided email is a valid and available email

        Args:
            email (str): user email
        Raises:
            (ValidationError): raise an exception if the email pattern doesn't
            correspond the provided email regex or if the email already exists in the database
        """

        errors = []

        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(email_regex, email.strip()):
            errors.append(get_error_body(email, INVALID_EMAIL_MSG, 'email'))
            raise_bad_request_error(errors)

        if User.query.filter(User.email == email.strip()).first():
            errors.append(get_error_body(email, TAKEN_EMAIL_MSG, 'email'))
            raise_conflict_error(errors)

    @classmethod
    def validate_password(cls, password):
        """
        Checks if the provided password is strong

        Args:
            password (str): user password
        Raises:
            (ValidationError): raise an exception if the password doesn't
            contain an uppercase letter, a lowercase letter, a digit or if
            the password length is less than 8
        """

        errors = [get_error_body(password, WEAK_PASSWORD_MSG, 'password')]

        is_upper = any(char.isupper() for char in password)
        is_lower = any(char.islower() for char in password)
        is_digit = any(char.isdigit() for char in password)

        if len(password) < 8 or not is_upper or not is_lower or not is_digit:
            raise_bad_request_error(errors)

    @classmethod
    def validate_username(cls, username):
        """
        Checks if the provided username is not taken

        Args:
            username (str): username
        Raises:
            (ValidationError): raise an exception if the username already exists in the database
        """

        errors = []
        if User.query.filter(User.username == username.strip()).first():
            errors.append(get_error_body(
                username, TAKEN_USERNAME_MSG, 'username'))
            raise_conflict_error(errors)

    @classmethod
    def validate_phone_number(cls, phone_number, user_id):
        """
        Checks if the phone number is a valid and available phone number

        Args:
            phone_number (str): user phone number
        Raises:
            (ValidationError): raise an exception if the phone number pattern doesn't
            correspond the provided phone number regex or if the phone number already 
            exists in the database
        """

        errors = []
        phone_regex = r"^(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$"
        if not re.match(phone_regex, phone_number.strip()):
            errors.append(get_error_body(
                phone_number, INVALID_PHONE_MSG, 'phone_number'))
            raise_bad_request_error(errors)

        user = User.query.filter(
            User.phone_number == phone_number.strip()).first()
        if user and user.id != user_id:
            errors.append(get_error_body(
                phone_number, TAKEN_PHONE_MSG, 'phone_number'))
            raise_conflict_error(errors)

    @classmethod
    def validate_user_request_body(cls, data: dict, keys):
        """ Validates the user request body """

        validate_request_body(data, keys)
        check_not_allowed_params(data, keys)

    @classmethod
    def validate_signup(cls, data: dict):
        """ Validates the user registration """

        keys = ['firstname', 'lastname', 'email', 'username', 'password']

        cls.validate_user_request_body(data, keys)
        cls.validate_email(data.get('email'))
        cls.validate_password(data.get('password'))
        cls.validate_username(data.get('username'))

    @classmethod
    def validate_password_reset(cls, data: dict):
        """ Validates the user password reset """

        keys = ['token', 'password']

        cls.validate_user_request_body(data, keys)
        cls.validate_password(data.get('password'))

    @classmethod
    def validate_profile_update(cls, data: dict, user_id):
        """ Validates the user profile update """

        required_keys = ['firstname', 'lastname']
        optional_keys = ['about', 'phone_number']
        allowed_keys = required_keys + optional_keys

        validate_request_body(data, required_keys)
        check_not_allowed_params(data, allowed_keys)

        phone_number = data.get('phone_number')
        if phone_number:
            cls.validate_phone_number(phone_number, user_id)

        if 'avatar' in request.files:
            validate_image('avatar', request.files['avatar'])
