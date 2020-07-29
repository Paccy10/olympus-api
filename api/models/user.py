""" Module for User Model """

from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import or_, and_

from .database import db
from .base import BaseModel


class User(BaseModel):
    """ User Model class """

    __tablename__ = 'users'

    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    about = db.Column(db.Text, nullable=True)
    avatar = db.Column(JSON, nullable=True)
    phone_number = db.Column(db.String(50), unique=True, nullable=True)

    @classmethod
    def find_user(cls, identifier):
        """ Finds a User instance by email or username """

        user = cls.query.filter(or_(and_(cls.email == identifier, cls.is_verified), and_(
            cls.username == identifier, cls.is_verified))).first()
        if user:
            return user
        return None
