from flask import Flask
from flask_restx import Api
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

    return app