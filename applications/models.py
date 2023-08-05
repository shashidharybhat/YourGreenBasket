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

<<<<<<< HEAD
class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, autoincrement=True, primary_key=True, unique=True)
    admin_name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    def get_id(self):
        return (self.admin_id)

    def __repr__(self) -> str:
        return f"Admin('{self.admin_name},{self.email}')"


class Venue(db.Model):
    __tablename__ = 'venue'
    venue_id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    venue_name = Column(String, unique=True, nullable=False)
    venue_loc = Column(String, nullable=False)
    venue_cap = Column(Integer)

    venue_shows = db.relationship('Shows', backref='venue')

    def __repr__(self) -> str:
        return f"Venue('{self.venue_name},{self.venue_loc},{self.venue_cap}')"


class Shows(db.Model):
    __tablename__ = 'shows'
    show_id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    show_name = Column(String, nullable=False)
    show_rating = Column(Float, default=0)
    num_rating = Column(Integer, default=0)
    show_price = Column(db.Float, nullable=False)
    show_desc = Column(String)
    show_date = Column(db.DateTime)
    show_venue = Column(Integer, db.ForeignKey('venue.venue_id'), nullable=False)
    show_cap = Column(Integer)
    show_current = Column(Integer, default=0)

    def __repr__(self):
        return f"Shows('{self.show_name},{self.show_price},{self.show_rating}')"
=======
>>>>>>> 0e3786b1bc399745604ec4d03d6566c90ea3d1fd
