import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(254), unique=True, nullable=False)
    _password_hash = db.Column(db.String(124))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    other = db.Column(db.Text, nullable=True)

    def __init__(self, email, password, other):
        self.email = email
        self.password = password
        self.other = other

    def __str__(self):
        return '<User %s>' % self.email

    @property
    def password(self):
        raise AttributeError()

    @password.setter
    def password(self, password):
        self._password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self._password_hash, password)

    def serialize(self):
        return {
            'email': self.email,
            'timestamp': self.timestamp,
            'other': self.other
        }



