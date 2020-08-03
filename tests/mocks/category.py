""" Module for category mocking data """

VALID_CATEGORY = {
    'name': 'house',
    'description': 'Living house'
}

INVALID_CATEGORY_WITHOUT_NAME = {
    'name': '',
    'description': ''
}

INVALID_CATEGORY_WITH_NOT_ALLOWED_PARAM = {
    'name': 'house',
    'description': '',
    'test': ''
}

INVALID_CATEGORY_WITH_EXISTED_NAME = {
    'name': 'apartment',
    'description': ''
}

INVALID_CATEGORY_WITH_INVALID_PARENT_ID = {
    'name': 'room',
    'description': '',
    'parent_id': 'test'
}

INVALID_CATEGORY_WITH_UNEXISTED_PARENT_ID = {
    'name': 'room',
    'description': '',
    'parent_id': 100
}
