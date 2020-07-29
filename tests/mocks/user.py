""" Module for user mocking data """

from api.utils.tokens_handler import generate_user_token

# Signup
VALID_USER = {
    'firstname': 'John',
    'lastname': 'Doe',
    'email': 'john.doe@app.com',
    'username': 'John',
    'password': 'Password1234'
}

INVALID_USER_WITHOUT_FIRSTNAME = {
    'firstname': '',
    'lastname': 'Doe',
    'email': 'john.doe@app.com',
    'username': 'John',
    'password': 'Password1234'
}

INVALID_USER_WITH__NOT_ALLOWED_PARAM = {
    'firstname': 'John',
    'lastname': 'Doe',
    'email': 'john.doe@app.com',
    'username': 'John',
    'password': 'Password1234',
    'is_admin': True
}

INVALID_USER_WITH_INVALID_EMAIL = {
    'firstname': 'John',
    'lastname': 'Doe',
    'email': 'john.doe@app',
    'username': 'John',
    'password': 'Password1234',
}

INVALID_USER_WITH_WEAK_PASSWORD = {
    'firstname': 'John',
    'lastname': 'Doe',
    'email': 'john.doe1@app.com',
    'username': 'John1',
    'password': 'pass',
}

INVALID_USER_WITH_EXISTED_USERNAME = {
    'firstname': 'John',
    'lastname': 'Doe',
    'email': 'john.doe1@app.com',
    'username': 'John',
    'password': 'Password1234',
}

# Login
USER_WITH_CORRECT_CREDENTIALS = {
    'username': 'John',
    'password': 'Password1234'
}

USER_WITH_INCORRECT_USERNAME = {
    'username': 'Kelly',
    'password': 'Password1234'
}

USER_WITH_INCORRECT_PASSWORD = {
    'username': 'John',
    'password': 'Password'
}

# Password Reset

RESET_REQUEST_USER = {
    'email': 'john.doe@app.com'
}

UNEXISTED_RESET_REQUEST_USER = {
    'email': 'kelly.doe@gmail.com'
}

RESET_PASSWORD_USER = {
    'password': 'Password@1234',
}

# Profile
PROFILE_USER = {
    'firstname': 'John',
    'lastname': 'Doe',
    'about': 'I am a software engineer',
    'phone_number': '0777777777'
}

PROFILE_USER_WITH_INVALID_PHONE = {
    'firstname': 'John',
    'lastname': 'Doe',
    'about': 'I am a software engineer',
    'phone_number': '07777'
}

PROFILE_USER_WITH_TAKEN_PHONE = {
    'firstname': 'John',
    'lastname': 'Doe',
    'about': 'I am a software engineer',
    'phone_number': '0777777777'
}
