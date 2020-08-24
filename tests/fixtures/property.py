""" Module for category fixtures """

import pytest

from api.models.property import Property


@pytest.fixture(scope='module')
def new_property(init_db, new_user, new_category, new_type):
    """ New property fixture """
    new_user.save()
    new_category.save()
    new_type.save()
    return Property(user_id=new_user.id,
                    category_id=new_category.id,
                    type_id=new_type.id,
                    title='test property',
                    address="test address",
                    longitude=123.4456,
                    latitude=-345.1233,
                    guests=2,
                    beds=2,
                    baths=2,
                    garages=1,
                    price=10000,
                    images=[],
                    is_published=True)


@pytest.fixture(scope='module')
def another_property(init_db, new_user, new_category, new_type):
    """ Another property fixture """
    new_user.save()
    new_category.save()
    new_type.save()
    return Property(user_id=new_user.id,
                    category_id=new_category.id,
                    type_id=new_type.id,
                    title='test property',
                    address="test address",
                    longitude=123.4456,
                    latitude=-345.1233,
                    guests=2,
                    beds=2,
                    baths=2,
                    garages=1,
                    price=10000,
                    images=[],
                    is_published=True)


@pytest.fixture(scope='module')
def unpublished_property(init_db, new_user, new_category, new_type):
    """ Another property fixture """
    new_user.save()
    new_category.save()
    new_type.save()
    return Property(user_id=new_user.id,
                    category_id=new_category.id,
                    type_id=new_type.id,
                    title='test property',
                    address="test address",
                    longitude=123.4456,
                    latitude=-345.1233,
                    guests=2,
                    beds=2,
                    baths=2,
                    garages=1,
                    price=10000,
                    images=[],
                    is_published=False)
