""" Module for property mocking data """

VALID_PROPERTY = {
    'title': 'Living house',
    'summary': '',
    'address': 'Kigali',
    'longitude': 123.3435,
    'latitude': -234.455,
    'guests': 2,
    'beds': 2,
    'baths': 1,
    'garages': 1,
    'price': 10000
}

INVALID_PROPERTY_WITH_UNEXISTED_CATEGORY = {
    'category_id': 100,
    'type_id': 100,
    'title': 'Living house',
    'address': 'Kigali',
    'longitude': 123.3435,
    'latitude': -234.455,
    'guests': 2,
    'beds': 2,
    'baths': 1,
    'garages': 1,
    'price': 10000
}

INVALID_PROPERTY_WITH_UNEXISTED_TYPE = {
    'type_id': 100,
    'title': 'Living house',
    'address': 'Kigali',
    'longitude': 123.3435,
    'latitude': -234.455,
    'guests': 2,
    'beds': 2,
    'baths': 1,
    'garages': 1,
    'price': 10000
}

INVALID_PROPERTY_WITH_STRING_LAT = {
    'title': 'Living house',
    'address': 'Kigali',
    'longitude': 123.3435,
    'latitude': "good",
    'guests': 2,
    'beds': 2,
    'baths': 1,
    'garages': 1,
    'price': 10000
}

INVALID_PROPERTY_WITH_INVALID_BED_NUM = {
    'title': 'Living house',
    'address': 'Kigali',
    'longitude': 123.3435,
    'latitude': -234.455,
    'guests': 2,
    'beds': -2,
    'baths': 1,
    'garages': 1,
    'price': 10000
}

INVALID_PROPERTY_WITHOUT_IMAGES = {
    'title': 'Living house',
    'address': 'Kigali',
    'longitude': 123.3435,
    'latitude': -234.455,
    'guests': 2,
    'beds': 2,
    'baths': 1,
    'garages': 1,
    'price': 10000
}
