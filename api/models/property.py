""" Module for Property Model """

from sqlalchemy.dialects.postgresql import JSON, ARRAY

from .database import db
from .base import BaseModel


class Property(BaseModel):
    """ Property Model class """

    __tablename__ = 'properties'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'categories.id'), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('types.id'), nullable=False)
    title = db.Column(db.String(250), nullable=False)
    summary = db.Column(db.Text, nullable=True)
    address = db.Column(db.String(250), nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    guests = db.Column(db.Integer, nullable=False, default=1)
    beds = db.Column(db.Integer, nullable=False, default=1)
    baths = db.Column(db.Integer, nullable=False, default=1)
    garages = db.Column(db.Integer, nullable=False, default=0)
    images = db.Column(ARRAY(JSON), nullable=False)
    video = db.Column(db.String, nullable=True)
    price = db.Column(db.DECIMAL(12, 2), nullable=False)
    is_published = db.Column(db.Boolean, default=False, nullable=False)

    owner = db.relationship('User', backref='property_owner', lazy='joined')
    category = db.relationship(
        'Category', backref='property_category', lazy='joined')
    property_type = db.relationship(
        'Type', backref='property_type', lazy='joined')
