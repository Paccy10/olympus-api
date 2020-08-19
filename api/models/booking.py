""" Module for Booking Model """

from .database import db
from .base import BaseModel


class Booking(BaseModel):
    """ Booking Model class """

    __tablename__ = 'bookings'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey(
        'properties.id'), nullable=False)
    checkin_date = db.Column(db.DateTime, nullable=False)
    checkout_date = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.DECIMAL(12, 2), nullable=False)
    status = db.Column(db.String(10), nullable=False, default='open')

    user = db.relationship('User', backref='booking_owner', lazy='joined')
    _property = db.relationship(
        'Property', backref='booking_property', lazy='joined')
