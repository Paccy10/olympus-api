""" Module for user mocking data """

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
