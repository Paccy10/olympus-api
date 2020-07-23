""" Module for testing app undefined route """

import app
from api.utils.helpers.messages.error import UNDEFINED_ROUTE


def test_app_undefined_route(client):
    """ Testing wrong route """

    response = client.get('/wrong-route')

    assert response.status_code == 404
    assert response.json['status'] == 'error'
    assert response.json['errors'][0]['value'] == '/wrong-route'
    assert response.json['errors'][0]['param'] == 'path'
    assert response.json['errors'][0]['message'] == UNDEFINED_ROUTE
