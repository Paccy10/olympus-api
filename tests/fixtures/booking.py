""" Module for category fixtures """


from datetime import datetime
import pytest

from api.models.booking import Booking
from api.utils.helpers.constants import DATE_FORMAT


@pytest.fixture(scope='module')
def new_booking(init_db, new_property, new_user):
    """ New property fixture """
    new_user.save()
    new_property.save()
    return Booking(user_id=new_user.id,
                   property_id=new_property.id,
                   checkin_date=datetime.strptime('2025-01-01', DATE_FORMAT),
                   checkout_date=datetime.strptime('2025-01-05', DATE_FORMAT),
                   price='50000')
