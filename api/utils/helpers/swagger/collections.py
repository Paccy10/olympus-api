""" Module for swagger collections """

from config.server import api

# Remove default namespace
api.namespaces.clear()

user_namespace = api.namespace(
    'Users',
    description='A Collection of User related endpoints',
    path='/users'
)

category_namespace = api.namespace(
    'Categories',
    description='A Collection of Category related endpoints',
    path='/categories'
)
