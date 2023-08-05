from applications.database import db
# from sqlalchemy import Column
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float
from main import login_manager
from flask_login import UserMixin
from flask import session


@login_manager.user_loader
def load_user(user_id):
    if session['acc_type'] == 'Admin':
        return Admin.query.get(int(user_id))
    elif session['acc_type'] == 'User':
        return User.query.get(int(user_id))
    else:
        return None


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    user_id = db.Column(Integer, autoincrement=True, primary_key=True, unique=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = Column(String(128), nullable=False)

    bookings = db.relationship('Shows', secondary='reservation', backref="user")

    def get_id(self):
        return self.user_id

    def __repr__(self) -> str:
        return f"User('{self.username}','{self.email}')"


class Reservation(db.Model):
    __tablename__ = 'reservation'
    reservation_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = Column(Integer, db.ForeignKey('user.user_id'), nullable=False)
    show_id = Column(Integer, db.ForeignKey('shows.show_id'), nullable=False)
    num_seats = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self) -> str:
        return f"Reservation('{self.user_id}','{self.show_id}','{self.num_seats}')"

