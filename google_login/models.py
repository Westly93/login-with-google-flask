from sqlalchemy.ext.declarative import declared_attr
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import URLSafeTimedSerializer
# from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import Text
from flask import current_app
from enum import Enum
from datetime import date
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from datetime import timedelta


db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstnames = db.Column(db.String(155), nullable=False)
    surname = db.Column(db.String(155), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    # image_file= db.Column(db.String(20), default= 'default.jpg')

    datecreated = db.Column(db.DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return f'{self.firstnames} {self.surname}'
