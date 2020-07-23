""" Main application module """

from flask import request
from flask_migrate import Migrate

from config.server import application
from api.utils.helpers.response import Response
from api.utils.helpers.messages.error import UNDEFINED_ROUTE
from api.utils.helpers import get_error_body
from api.models.database import db
from api.models.user import User
import api.views.user

migrate = Migrate(application, db)


@application.errorhandler(404)
def page_not_found(error):
    """ Undefined route handler """

    errors = [get_error_body(request.path, UNDEFINED_ROUTE, 'path', 'url')]

    return Response.error(errors, 404)


if __name__ == '__main__':
    application.run()
