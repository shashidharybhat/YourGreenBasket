from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, BooleanField, DecimalField, TextAreaField, \
    IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, email_validator, ValidationError, Optional
from wtforms.fields import DateTimeLocalField
from applications.models import *
from flask_login import current_user


class Registration(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That Username is taken! Please try a different one")
        if ' ' in username.data:
            raise ValidationError("White spaces are not allowed in the Username")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That Email is taken!")


class Login(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log in')


class EditShow(FlaskForm):
    name = StringField("Show Name", validators=[Optional()])
    price = DecimalField("Price: $", validators=[Optional()])
    desc = TextAreaField("Show Description", validators=[Optional()])
    datetime = DateTimeLocalField("Date and Time", format='%Y-%m-%dT%H:%M', validators=[Optional()])
    cap = IntegerField("Capacity", validators=[Optional()])
    current_cap = IntegerField("Current Bookings", validators=[Optional()])
    submit = SubmitField('Update Show')

