from flask import Flask, send_from_directory
from flask_restx import Api
from flask_cors import CORS
from app.extensions import bcrypt, jwt, db
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenity_ns
from app.api.v1.places import api as place_ns
from app.api.v1.reviews import api as review_ns
from app.api.v1.auth import api as auth_ns
from config import config



def create_app(config_class=config['development']):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize CORS with support for all routes and origins
    CORS(app, resources={r"/*": {"origins": "*"}})

    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600
    authorizations = {
        'Bearer': {'type': 'apiKey','in': 'header','name': 'Authorization', 'description': 'JWT Token'}
    }
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', authorizations=authorizations, security='Bearer')

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenity_ns, path='/api/v1/amenities')
    api.add_namespace(place_ns, path='/api/v1/places')
    api.add_namespace(review_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1')
    
    # Add route for serving static files from base_files directory
    @app.route('/')
    def index():
        return send_from_directory('../base_files', 'index.html')
        
    @app.route('/<path:path>')
    def static_files(path):
        return send_from_directory('../base_files', path)

    return app