""" Module for common helpers """


def get_error_body(value, message, param, location='body'):
    """
    Returns a well formed error body

    Args:
        value (): param value
        message (str): error message
        param (str): param that is causing the error
        location (str): location of the param
    Return:
        (dict): dict with value, message, param and location properties
    """
    return {
        'value': value,
        'message': message,
        'param': param,
        'location': location
    }


def request_data_strip(request_data):
    """
    Removes spaces at the beginning and at the end of request data values
    Args:
        request_data(dict): request body

    Returns:
        request_data(dict): request body with removed spaces
    """

    for key, value in request_data.items():
        if isinstance(value, str):
            request_data[key] = value.strip()

    return request_data
