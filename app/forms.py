from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
from wtforms import ValidationError

from app.models import User


class RegistrationForm(Form):

    email = StringField('Email', description='Email',
                        validators=[DataRequired('Email is required'), Email()])
    password = PasswordField('Password', description='Password',
                             validators=[DataRequired('Password is required'),
                                         Length(6, 20, message="Password length must be between 6 and 20 characters")])
    other = TextAreaField('Other information:', description='Other information')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
