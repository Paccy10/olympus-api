""" Module for endpoints responses """


class Response:
    """ Response class """

    @classmethod
    def success(cls, message, data, code):
        """ success response

            Args:
                message (string): response message property
                data (dict): response data property
                code (dict): response status code
            Returns:
                (dict): dictionary with status, message and data properties
        """
        return {
            'status': 'success',
            'message': message,
            'data': data
        }, code

    @classmethod
    def error(cls, errors, code):
        """ error response

            Args:
                message (string): response message property
                data (list): response data property
                code (dict): response status code
            Returns:
                (dict): dictionary with status, message and data properties
        """
        return {
            'status': 'error',
            'errors': errors
        }, code
