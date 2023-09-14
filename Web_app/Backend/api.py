from flask import Blueprint
from flask_restful import Api
from .auth import SignUp, Login, Logout
from .views import Home, Venue, Show, Booking, Export_venues, Search


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Authorisation API
api.add_resource(SignUp, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')

# Home API
api.add_resource(Home, '/home')

# Venue API
api.add_resource(Venue, '/venue')

# Show API
api.add_resource(Show, '/show')

# Booking API
api.add_resource(Booking, '/bookings')

# Export APT
api.add_resource(Export_venues, '/export')

# Search API
api.add_resource(Search, '/search')
