""" Module for pagination handler """

from flask import request

from .validators import validate_positive_integer


def get_pagination_params():
    """
    Generates the pagination params

    Returns:
        dict: page and limit data
    """

    page = request.args.get('page')
    limit = request.args.get('limit')

    if page is None:
        page = 1

    if limit is None:
        limit = 10

    if page is not None:
        validate_positive_integer('page', page, location='url')

    if limit is not None:
        validate_positive_integer('limit', limit, location='url')

    return int(page), int(limit)


def paginate_resource(model, schema, condition):
    """
    Paginate the given resource
    Args:
        model: resource model
        schema: model schema

    Returns:
        dict: paginated data and metadata
    """

    page, limit = get_pagination_params()
    records_query = model.query.filter(
        condition).paginate(page=page, max_per_page=limit)
    data = schema.dump(records_query.items)
    metadata = {
        'current_page': records_query.page,
        'next_page': records_query.next_num,
        'prev_page': records_query.prev_num,
        'pages_count': records_query.pages,
        'records_count': records_query.total
    }

    return data, metadata
