""" Module for Type Model """

from .database import db
from .base import BaseModel


class Type(BaseModel):
    """ Type Model class """

    __tablename__ = 'types'

    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
