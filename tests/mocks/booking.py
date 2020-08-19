""" Module for booking mocking data """

VALID_BOOKING = {
    'checkin_date': '2025-01-01',
    'checkout_date': '2025-01-05'
}

INVALID_BOOKING_WITH_INVALID_DATES = {
    'checkin_date': '01-01-2020',
    'checkout_date': '01-01-2020'
}

INVALID_BOOKING_WITH_PAST_CHECKIN_DATE = {
    'checkin_date': '2020-08-01',
    'checkout_date': '2020-08-05'
}

INVALID_BOOKING_WITH_LOWER_CHECKOUT_DATE = {
    'checkin_date': '2025-01-05',
    'checkout_date': '2025-01-01'
}
