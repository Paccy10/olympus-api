""" Main application module """

from flask import request
from flask_migrate import Migrate

from config.server import application
from api.utils.helpers.response import Response
from api.utils.helpers.messages.error import UNDEFINED_ROUTE_MSG
from api.utils.helpers import get_error_body
from api.models.database import db
from api.models.user import User
from api.models.category import Category
from api.models.type import Type
from api.models.property import Property
import api.views.user
import api.views.category
import api.views.type
import api.views.property

migrate = Migrate(application, db)


@application.errorhandler(404)
def page_not_found(error):
    """ Undefined route handler """

    errors = [get_error_body(request.path, UNDEFINED_ROUTE_MSG, 'path', 'url')]

    return Response.error(errors, 404)


if __name__ == '__main__':
    application.run()
