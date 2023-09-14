from .database import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import date


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String(150),unique = True, nullable = False)
    password = db.Column(db.String(150), nullable = False)
    name = db.Column(db.String(150), nullable = False)
    isadmin = db.Column(db.Boolean, default = False)
    venues = db.relationship('Venue')
    bookings = db.relationship('Booking')

    def __repr__(self) -> str:
        return f"<User name={self.name} email={self.email} isadmin={self.isadmin} venues={self.venues}>"


class Venue (db.Model):
    venue_id = db.Column(db.Integer, primary_key = True)
    venue_name = db.Column(db.String(250), nullable = False)
    place = db.Column(db.String(250), nullable = False)
    capacity = db.Column(db.Integer)
    owner = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable = False)
    shows = db.relationship('Show',cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f"<id = {self.venue_id} Venue name={self.venue_name} place={self.place} capacity={self.capacity} owner={self.owner} shows = {self.shows}"


class Show(db.Model):
    show_id = db.Column(db.Integer, primary_key = True)
    show_name = db.Column(db.String(250))
    rating = db.Column(db.Integer)
    start_time = db.Column(db.Time(timezone = True), default = func.now())
    end_time = db.Column(db.Time(timezone = True), default = func.now())
    tags = db.Column(db.String(1000))
    price = db.Column(db.Integer)
    booked_tickets = db.Column(db.Integer, default=0)
    hall = db.Column(db.Integer, db.ForeignKey('venue.venue_id', ondelete = 'CASCADE'), nullable = False)
    book_ings = db.relationship('Booking', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f"<id = {self.show_id} show_name = {self.show_name} rating = {self.rating} booked_tickets = {self.booked_tickets} >"
        
class Booking(db.Model):
    booking_id = db.Column(db.Integer, primary_key = True)
    tickets = db.Column(db.Integer)
    booking_date = db.Column(db.Date, default=date.today)
    show = db.Column(db.Integer, db.ForeignKey('show.show_id', ondelete = 'CASCADE'), nullable = False)
    user = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable = False)

    def __repr__(self) -> str:
        return f"<id = {self.booking_id} tickets = {self.tickets} show = {self.show}"



  