""" Module for error messages """

UNDEFINED_ROUTE_MSG = 'The requested route is not defined'
KEY_REQUIRED_MSG = 'The {} is required'
KEY_NOT_ALLOWED_MSG = 'The {} is not allowed'
NOT_INTEGER_MSG = 'The {} must be a positive integer'

# Users
INVALID_EMAIL_MSG = 'The email provided is not a valid email'
WEAK_PASSWORD_MSG = 'Weak password. The password must be 8 characters long '\
                    'and it must contain at least one upper case letter, one'\
                    'lower case letter and one number'
TAKEN_EMAIL_MSG = 'The provided email already exists'
TAKEN_USERNAME_MSG = 'The provided username already exists'
INVALID_USER_TOKEN_MSG = 'The user verification token has expired'
ALREADY_VERIFIED_MSG = 'User account already verified'
USER_NOT_FOUND_MSG = 'User account not found'
INVALID_CREDENTIALS = 'Invalid credentials'
INVALID_PHONE_MSG = 'The phone number provided is not a valid phone number'
TAKEN_PHONE_MSG = 'The provided phone number is already taken'
NO_AUTH_TOKEN_MSG = 'No authorization token provided'
INVALID_AUTH_TOKEN_MSG = 'The provided authorization token is invalid'
NO_BEARER_IN_TOKEN_MSG = "The token should begin with the word 'Bearer'"
EXPIRED_AUTH_TOKEN_MSG = 'The authorization token has expired'
NOT_IMAGE_EXT_MSG = 'The uploaded file is not allowed'
UNAUTHORIZED_MSG = 'Permission denied. You are not authorized to perform this action'

# Categories
TAKEN_CATEGORY_NAME_MSG = 'The provided category name already exists'
CATEGORY_NOT_FOUND_MSG = 'Category not found'