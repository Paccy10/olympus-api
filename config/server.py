""" Module for Server configuration """

from flask import Flask, Blueprint
from flask_restx import Api

from .environment import AppConfig

api_blueprint = Blueprint('api_blueprint', __name__, url_prefix='/api/v1')

authorizations = {
    'Auth Token': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(api_blueprint,
          title='Olympus App API',
          description='Vacation rental online marketplace app API',
          security='Auth Token',
          doc='/documentation',
          authorizations=authorizations)


def create_app(config=AppConfig):
    """ Create the flask application """

    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(api_blueprint)

    return app


application = create_app()
