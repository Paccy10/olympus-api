""" Module for swagger responses """

responses = {
    200: 'Success',
    201: 'Created',
    401: 'Unauthorized Error',
    400: 'Validation Error',
    403: 'Forbidden Error',
    404: 'Not Found Error',
    409: 'Conflict Error',
}


def get_responses(*args):
    """ swagger responses

        Args:
            args (int): responses status codes
        Returns:
            (dict): dictionary with possible responses
    """

    result = {}
    for code in args:
        result[code] = responses.get(code)

    return result
