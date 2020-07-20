""" Main application module """

from config.server import application


@application.errorhandler(404)
def page_not_found(error):
    """ Undefined route handler """

    return {
        'status': 'error',
        'message': 'Undefined route'
    }, 404


if __name__ == '__main__':
    application.run()
