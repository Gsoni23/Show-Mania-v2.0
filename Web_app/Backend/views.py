from flask import Blueprint, request
from flask_restful import Resource, reqparse, abort, fields, marshal_with
from functools import wraps #Used to make a decorator for RBAC 
from flask_jwt_extended import jwt_required, get_jwt_identity, get_current_user
from . import models
from .database import db
from datetime import datetime
from .worker import export_data
import time
from .cache import cache

views = Blueprint('views',__name__)

# This Decorator is used to implement RBAC (Role Based Access Control)
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not get_current_user().isadmin:
            abort(403, description = "You are not authorized to perform this action")
        return f(*args, **kwargs)
    return decorated_function

search_parser = reqparse.RequestParser()

home_fields = {
    "user_id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    "isadmin": fields.Boolean,
    "venues": fields.List(fields.Nested({
        "venue_id": fields.Integer,
        "venue_name": fields.String,
        "place": fields.String,
        "capacity": fields.Integer,
        "owner": fields.Integer,
        "shows": fields.List(fields.Nested({
            "show_id": fields.Integer,
            "show_name": fields.String,
            "rating": fields.Integer,
            "start_time": fields.String,
            "end_time": fields.String,
            "tags": fields.String,
            "price": fields.Integer,
            "booked_tickets": fields.Integer,
            "hall": fields.Integer,
            "bookings": fields.List(fields.Nested({
                "booking_id": fields.Integer,
                "tickets": fields.Integer,
                "show_id": fields.Integer,
                "venue_id": fields.Integer,
                "user_id": fields.Integer
            }))
        }))
    })),
    }



class Home(Resource):

    @jwt_required()
    @marshal_with(home_fields)
    def get(self):
        current_user = get_current_user()
        if current_user.isadmin: 
            return current_user, 200
        else:
            venues = db.session.query(models.Venue).all()
            current_user.venues = venues
            return current_user, 200


class Venue(Resource):

    venue_fields = {
    "venue_name": fields.String,
    "place": fields.String,
    "capacity": fields.Integer,
    }

    @jwt_required()
    @admin_required
    @marshal_with(venue_fields)
    def get(self):
        venue_id = request.args.get('venue_id')
        venue = models.Venue.query.get(int(venue_id))
        if not venue:
            return {"message": "Venue not found"}, 404
        else:
            return venue, 200


    venue_post_parser = reqparse.RequestParser()
    venue_post_parser.add_argument("venue_name", type=str, help="Venue name is required", required=True)
    venue_post_parser.add_argument("place", type=str, help="Venue place is required", required=True)
    venue_post_parser.add_argument("capacity", type=int, help="Capacity of the Venue is required", required=True)


    @jwt_required()
    @admin_required
    def post(self):

        req_args = self.venue_post_parser.parse_args()
        venue_name = req_args["venue_name"]
        place = req_args["place"]
        capacity = req_args["capacity"]

        new_venue = models.Venue(venue_name = venue_name, place = place, capacity = capacity, owner = get_current_user().user_id)
        db.session.add(new_venue)
        db.session.commit()
        return {"message": "Venue added successfully"}, 200


    venue_patch_parser = reqparse.RequestParser()
    venue_patch_parser.add_argument("venue_id", type=int, help="Venue id is required", required=True)
    venue_patch_parser.add_argument("venue_name", type=str, help="Venue name is required", required=True)
    venue_patch_parser.add_argument("place", type=str, help="Venue place is required", required=True)
    venue_patch_parser.add_argument("capacity", type=int, help="Capacity of the Venue is required", required=True)

    @jwt_required()
    @admin_required
    def patch(self):
        
        req_args = self.venue_patch_parser.parse_args()
            
        venue_id = req_args["venue_id"]
        venue_name = req_args["venue_name"]
        place = req_args["place"]
        capacity = req_args["capacity"]

        venue = models.Venue.query.filter_by(venue_id = venue_id).first()
        if not venue:
            return {"message": "Venue not found"}, 404
        else:
            venue.venue_name = venue_name
            venue.place = place
            venue.capacity = capacity
            db.session.commit()

            return {"message": "Venue updated successfully"}, 200
        
    
    @jwt_required()
    @admin_required
    def delete(self):
        
        venue_id = request.args.get('venue_id')
        venue = models.Venue.query.get(int(venue_id))
        
        if venue:
            db.session.delete(venue)
            db.session.commit()

            return {"message": "Venue deleted successfully"}, 200

        else:
            return {"message": "Venue not found"}, 404



class Show(Resource):

    show_fileds = {
    "show_name": fields.String,
    "rating": fields.Integer,
    "start_time": fields.String,
    "end_time": fields.String,
    "tags": fields.String,
    "price": fields.Integer,
    "booked_tickets": fields.Integer}

    

    @jwt_required()
    @admin_required
    @marshal_with(show_fileds)
    def get(self):
        show_id = request.args.get('show_id')
        show = models.Show.query.get(int(show_id))
        if not show:
            return {"message": "Show not found"}, 404
        else:
            return show, 200


    show_post_parser = reqparse.RequestParser()
    show_post_parser.add_argument("show_name", type=str, help="Show name is required", required=True)
    show_post_parser.add_argument("rating", type=int, help="Rating is required", required=True)
    show_post_parser.add_argument("venue_id", type=int, help="Venue id is required", required=True)
    show_post_parser.add_argument('start_time', type=lambda x: datetime.strptime(x, '%H:%M').time())
    show_post_parser.add_argument('end_time', type=lambda x: datetime.strptime(x, '%H:%M').time())
    show_post_parser.add_argument('tags', type=str, help="Tags are required", required=True)
    show_post_parser.add_argument('price', type=int, help="Ticket price is required", required=True)

    @jwt_required()
    @admin_required
    def post(self):

        req_args = self.show_post_parser.parse_args()
        show_name = req_args["show_name"]
        rating = req_args["rating"]
        venue_id = req_args["venue_id"]
        start_time = req_args["start_time"]
        end_time = req_args["end_time"]
        tags = req_args["tags"]
        price = req_args["price"]

        venue = models.Venue.query.filter_by(venue_id = venue_id).first()
        if not venue:
            return {"message": "Venue not found"}, 404
        else:
            new_show = models.Show(show_name = show_name, rating = rating, start_time = start_time, end_time = end_time, tags = tags, price = price, hall = venue_id)
            db.session.add(new_show)
            db.session.commit()
            return {"message": "Show added successfully"}, 200



    show_patch_parser = reqparse.RequestParser()
    show_patch_parser.add_argument("show_name", type=str, help="Show name is required", required=True)
    show_patch_parser.add_argument("rating", type=int, help="Rating is required", required=True)
    show_patch_parser.add_argument('start_time', type=lambda x: datetime.strptime(x, '%H:%M').time())
    show_patch_parser.add_argument('end_time', type=lambda x: datetime.strptime(x, '%H:%M').time())
    show_patch_parser.add_argument('tags', type=str, help="Tags are required", required=True)
    show_patch_parser.add_argument('price', type=int, help="Ticket price is required", required=True)

    @jwt_required()
    @admin_required
    def patch(self):
        
        show_id = request.args.get('show_id')
        req_args = self.show_patch_parser.parse_args()

        show_name = req_args["show_name"]
        rating = req_args["rating"]
        start_time = req_args["start_time"]
        end_time = req_args["end_time"]
        tags = req_args["tags"]
        price = req_args["price"]

        show = models.Show.query.get(int(show_id))
        if not show:
            return {"message": "Show not found"}, 404
        
        else:
            show.show_name = show_name
            show.rating = rating
            show.start_time = start_time
            show.end_time = end_time
            show.tags = tags
            show.price = price

            db.session.commit()

            return {"message": "Show updated successfully"}, 200

    
    
    @jwt_required()
    @admin_required
    def delete(self):
        
        show_id = request.args.get('show_id')
        show = models.Show.query.get(int(show_id))

        if not show:
            return {"message": "Show not found"}, 404
        else:
            db.session.delete(show)
            db.session.commit()

            return {"message": "Show deleted successfully"}, 200
            

            
class Booking(Resource):

    booking_fields = {
        "bookings": fields.List(fields.Nested({
            "booking_id": fields.Integer,
            "show_name": fields.String,
            "venue_name": fields.String,
            "venue_location": fields.String,
            "start_time": fields.String,
            "end_time": fields.String,
            "rating": fields.Integer,
            "tickets": fields.Integer,
        }))
    }

    
    @jwt_required()
    @marshal_with(booking_fields)
    # uncomment below line to demonstrate caching in the project.
    # @cache.cached(timeout=600)  # Cache this route for 10 minutes
    def get(self):
        
        user_id = get_jwt_identity()
        bookings = models.Booking.query.filter_by(user=user_id).all()

        formatted_bookings = []
        for booking in bookings:
            show = models.Show.query.filter_by(show_id = int(booking.show)).first()
            venue = models.Venue.query.filter_by(venue_id = int(show.hall)).first()

            formatted_booking = {
                "booking_id": booking.booking_id,
                "show_name": show.show_name,
                "venue_name": venue.venue_name,
                "venue_location": venue.place,
                "start_time": show.start_time,
                "end_time": show.end_time,
                "rating": show.rating,
                "tickets": booking.tickets
            }

            formatted_bookings.append(formatted_booking)
        return {"bookings": formatted_bookings}, 200


    booking_post_parser = reqparse.RequestParser()
    booking_post_parser.add_argument("venue_id", type=int, help="Venue id is required", required=True)
    booking_post_parser.add_argument("show_id", type=int, help="Show id is required", required=True)
    booking_post_parser.add_argument("tickets", type=int, help="Number of tickets is required", required=True)

    

    @jwt_required()
    def post(self):
        req_args = self.booking_post_parser.parse_args()
        venue_id = req_args["venue_id"]
        show_id = req_args["show_id"]
        tickets = req_args["tickets"]

        # Check if the venue exists
        venue = models.Venue.query.get(venue_id)
        if not venue:
            return {"message": "Venue not found"}, 404

        # Check if the show exists
        show = models.Show.query.get(show_id)
        if not show:
            return {"message": "Show not found"}, 404

        # Check if the venue has reached its capacity
        if show.booked_tickets + tickets > venue.capacity:
            return {"message": "Venue has reached its capacity"}, 403

        # Create a new booking
        user_id = get_jwt_identity()
        new_booking = models.Booking(tickets=tickets, show=show_id, user=user_id)
        db.session.add(new_booking)
        db.session.commit()

        # Update the booked tickets count for the show
        show.booked_tickets += tickets
        db.session.commit()

        return {"message": "Booking created successfully"}, 200

# Use to get data for search results in home page
class Search(Resource):

        search_show_fields = {
        "shows": fields.List(fields.Nested({
            'show_id': fields.Integer,
            'show_name': fields.String,
            'rating': fields.Float,
            'tags': fields.String,
            'price': fields.Integer,
            'venue_id': fields.Integer}))
        }

        @jwt_required()
        @marshal_with(search_show_fields)
        def get(self):
            search_query = request.args.get('searchQuery')
            
            shows = models.Show.query.filter((models.Show.rating.like("%"+search_query+"%")) | (models.Show.show_name.like("%"+search_query+"%")) | (models.Show.tags.like("%"+search_query+"%"))).all()
            
            formatted_show_list = []
            for show in shows:
                formatted_show = {
                    'show_id': show.show_id,
                    'show_name': show.show_name,
                    'rating': show.rating,
                    'tags': show.tags,
                    'price': show.price,
                    'venue_id': show.hall,
                }
                formatted_show_list.append(formatted_show)

            return { "shows" : formatted_show_list}, 200
            



# to export the venues data in csv format to the admin
class Export_venues(Resource):

    @jwt_required()
    @admin_required
    def get(self):
        venue_id = request.args.get('venue_id')

        res = export_data.delay(venue_id)

        while not res.ready():
            print("Still in progress")
            print(venue_id)

            time.sleep(2)

        if not res.get()[0] : 
            return {"message" : res.get()[1]},400
        else:
            return {"message" : res.get()[1]},200
       

